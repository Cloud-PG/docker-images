# DODAS CMSSW jobs emulator

Emulate CMS MC production jobs to verify that the node is actually able to run real workflows as in DODAS HTCondor environment.

The job starts up the CMSSW runtime and exit with 0 in case of success.

## Usage

```bash
docker run --name cmssw_test cloudpg/cmssw:mc-test
```

Gathering logs:

```bash
docker logs cmssw_test
```

## DODAS architecture

For an overview of the DODAS architecture please refers to this link:

- [DODAS documentation site](https://dodas-ts.github.io/dodas-doc/)
