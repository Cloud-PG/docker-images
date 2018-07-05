import FWCore.ParameterSet.Config as cms

process = cms.Process("IOTest")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = '80X_dataRun2_Prompt_ICHEP16JEC_v0'
process.GlobalTag.globaltag = '94X_dataRun2_ReReco_EOY17_v2'
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))
process.MessageLogger = cms.Service("MessageLogger")


process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('testme.root'
#'root://xrootd.echo.stfc.ac.uk//store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/904DDAFE-5096-E711-B0EB-FA163ECCB08D.root'
#'/store/mc/HC/GenericTTbar/GEN-SIM-RECO/CMSSW_7_0_4_START70_V7-v1/00000/C44C3853-38CD-E311-88B1-02163E00E8E6.root'
#'/store/data/Run2017F/ZeroBias/AOD/17Nov2017-v1/70005/5EB66B8A-D1DF-E711-B76A-008CFAE45228.root'
#  '/store/data/Run2017F/ZeroBias/AOD/PromptReco-v1/000/305/033/00000/9A0EE12B-D2B1-E711-AD85-02163E01410E.root'
)##,
##skipEvents = cms.untracked.uint32(3800)
)

process.demo = cms.EDAnalyzer('IOTest')


process.TFileService = cms.Service("TFileService",

  fileName = cms.string('DS2b_17.root')
)


process.p = cms.Path(process.demo)
