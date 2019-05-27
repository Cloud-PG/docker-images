# DODAS CMSSW jobs emulator

Emulate CMS MC production jobs to verify that the node is actually able to run real workflows as in DODAS environment.

The job start up the CMSSW runtime and exit with 0 in case of success.

## Usage

```docker run -v $PWD/inputfile.root:/CMSSW/testme.root dciangot/cmssw:mc-test```

## DODAS architecture

For an overview of the DODAS architecture please refers to this link:

- [DODAS documentation site](https://dodas-ts.github.io/dodas-doc/)
