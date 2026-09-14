from types import SimpleNamespace

from web_status_watcher import app


class FakeLogger:
    def __init__(self) -> None:
        self.messages = []

    def info(self, *args, **kwargs) -> None:
        self.messages.append(("info", args))

    def warning(self, *args, **kwargs) -> None:
        self.messages.append(("warning", args))

    def error(self, *args, **kwargs) -> None:
        self.messages.append(("error", args))

    def exception(self, *args, **kwargs) -> None:
        self.messages.append(("exception", args))


class FakeDatabase:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.sites = SimpleNamespace(
            get_all=lambda: []
        )

    def connect(self) -> None:
        pass

    def execute(self, *args, **kwargs) -> None:
        pass

    def close(self) -> None:
        pass


class FakeConfig:
    def __init__(self, config_dir) -> None:
        self.data = {
            "purchase": {
                "enabled": True,
                "product_url": (
                    "https://coins.bank.gov.ua/"
                    "arhistratig-mihajil-c-/p-1126.html?cid=14348"
                ),
                "products_id": 1126,
                "quantity": 1,
            }
        }


class FakeWorker:
    def __init__(self) -> None:
        self.name = "purchase"
        self.interval = 1
        self.running = True

    def tick(self) -> None:
        self.running = False


class FakeScheduler:
    last_instance = None

    def __init__(self) -> None:
        type(self).last_instance = self

        self.workers = []
        self.start_calls = 0
        self.stop_calls = 0

    def add_worker(
        self,
        worker,
    ) -> None:
        self.workers.append(worker)

    def start(self) -> None:
        self.start_calls += 1

        if self.workers:
            self.workers[0].tick()

    def stop(self) -> None:
        self.stop_calls += 1


fake_logger = FakeLogger()
fake_worker = FakeWorker()

original_logger = app.get_logger
original_config = app.ConfigManager
original_database = app.Database
original_validate = app.validate
original_target_factory = app.PurchaseTargetFactory
original_worker_factory = app.PurchaseWorkerFactory
original_scheduler = app.Scheduler


app.get_logger = lambda: fake_logger
app.ConfigManager = FakeConfig
app.Database = FakeDatabase
app.validate = lambda data: None

app.PurchaseTargetFactory = SimpleNamespace(
    create=lambda config: SimpleNamespace(
        enabled=True
    )
)

app.PurchaseWorkerFactory = SimpleNamespace(
    create=lambda config: fake_worker
)

app.Scheduler = FakeScheduler


try:
    app.main()

finally:
    app.get_logger = original_logger
    app.ConfigManager = original_config
    app.Database = original_database
    app.validate = original_validate
    app.PurchaseTargetFactory = original_target_factory
    app.PurchaseWorkerFactory = original_worker_factory
    app.Scheduler = original_scheduler


scheduler = FakeScheduler.last_instance

assert scheduler is not None

assert scheduler.start_calls == 1
assert scheduler.stop_calls == 1

assert len(scheduler.workers) == 1
assert scheduler.workers[0] is fake_worker

assert fake_worker.running is False

assert any(
    "Purchase worker registered" in message
    for level, args in fake_logger.messages
    if args
    for message in args
    if isinstance(message, str)
)

assert any(
    "Purchase scheduler started" in message
    for level, args in fake_logger.messages
    if args
    for message in args
    if isinstance(message, str)
)

assert any(
    "Purchase scheduler stopped" in message
    for level, args in fake_logger.messages
    if args
    for message in args
    if isinstance(message, str)
)


print()
print(
    "APP PURCHASE SCHEDULER TEST PASSED"
)
print(
    "worker registered -> True"
)
print(
    "scheduler.start() -> 1"
)
print(
    "scheduler.stop() -> 1"
)
print(
    "worker.running after tick -> False"
)