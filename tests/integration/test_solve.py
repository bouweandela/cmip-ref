import cmip_ref.solver
from cmip_ref.database import Database
from cmip_ref.models import Dataset, MetricExecution
from cmip_ref.provider_registry import ProviderRegistry, _register_provider


class ExampleProviderRegistry(ProviderRegistry):
    def build_from_db(db: Database) -> "ExampleProviderRegistry":
        """
        Create a ProviderRegistry instance containing only the Example provider.

        Parameters
        ----------
        db
            Database instance

        Returns
        -------
        :
            A new ProviderRegistry instance
        """
        # TODO: We don't yet have any tables to represent metrics providers
        from cmip_ref_metrics_example import provider as example_provider

        with db.session.begin_nested():
            _register_provider(db, example_provider)
        return ProviderRegistry(providers=[example_provider])


def test_solve(sample_data_dir, config, invoke_cli, monkeypatch):
    db = Database.from_config(config)
    monkeypatch.setattr(cmip_ref.solver, "ProviderRegistry", ExampleProviderRegistry)
    invoke_cli(["datasets", "ingest", "--source-type", "cmip6", str(sample_data_dir)])
    assert db.session.query(Dataset).count() == 10

    result = invoke_cli(["--verbose", "solve"])
    assert "Created metric execution ACCESS-ESM1-5_rsut_ssp126_r1i1p1f1" in result.stderr
    assert "Running metric" in result.stderr
    assert db.session.query(MetricExecution).count() == 4

    # Running solve again should not trigger any new metric executions
    result = invoke_cli(["--verbose", "solve"])
    assert "Created metric execution ACCESS-ESM1-5_rsut_ssp126_r1i1p1f1" not in result.stderr
    assert db.session.query(MetricExecution).count() == 4
    execution = db.session.query(MetricExecution).filter_by(key="ACCESS-ESM1-5_rsut_ssp126_r1i1p1f1").one()

    assert len(execution.results[0].datasets) == 1
    assert (
        execution.results[0].datasets[0].instance_id
        == "CMIP6.ScenarioMIP.CSIRO.ACCESS-ESM1-5.ssp126.r1i1p1f1.Amon.rsut.gn.v20210318"
    )
