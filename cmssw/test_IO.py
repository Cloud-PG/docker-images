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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))
process.MessageLogger = cms.Service("MessageLogger")

process.Timing = cms.Service("Timing",
  summaryOnly = cms.untracked.bool(False),
  useJobReport = cms.untracked.bool(True)
)


process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('testme.root')
)

process.demo = cms.EDAnalyzer('IOTest')


process.TFileService = cms.Service("TFileService",

  fileName = cms.string('DS2b_17.root')
)


process.p = cms.Path(process.demo)
