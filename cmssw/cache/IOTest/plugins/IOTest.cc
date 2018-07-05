// -*- C++ -*-
//
// Package:    cache/IOTest
// Class:      IOTest
// 
/**\class IOTest IOTest.cc cache/IOTest/plugins/IOTest.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Diego Ciangottini
//         Created:  Mon, 26 Mar 2018 08:29:37 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include <memory>
#include <map>
#include <string>
#include <vector>
#include <iostream>
#include <algorithm>

#include "TH1.h"
#include "TH2.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TVector3.h"
#include "TVector2.h"
#include "TTree.h"
#include "TProfile.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Version/interface/GetReleaseVersion.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "FWCore/Framework/interface/ESWatcher.h"

#include "SimDataFormats/Vertex/interface/SimVertexContainer.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/Track/interface/SimTrackContainer.h"
#include "SimDataFormats/Track/interface/SimTrack.h"

#include "SimTracker/Records/interface/TrackAssociatorRecord.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/VertexCompositeCandidate.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/PatCandidates/interface/TriggerEvent.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHitFwd.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
#include "DataFormats/TrackCandidate/interface/TrackCandidateCollection.h"
#include "DataFormats/EgammaReco/interface/ElectronSeed.h"
#include "DataFormats/EgammaReco/interface/ElectronSeedFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/Common/interface/getRef.h"
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/SiStripDetId/interface/TIBDetId.h"
#include "DataFormats/SiStripDetId/interface/TIDDetId.h"
#include "DataFormats/SiStripDetId/interface/TOBDetId.h"
#include "DataFormats/SiStripDetId/interface/TECDetId.h"
#include "DataFormats/Common/interface/OwnVector.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/TrackReco/interface/DeDxData.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Common/interface/TriggerResults.h"

#include <DataFormats/BeamSpot/interface/BeamSpot.h>
#include <DataFormats/VertexReco/interface/VertexFwd.h>
#include <DataFormats/Common/interface/Ref.h>
#include <DataFormats/Math/interface/deltaPhi.h>
#include <DataFormats/Common/interface/Ptr.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h>
#include <DataFormats/VertexReco/interface/Vertex.h>

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Statistics/interface/ChiSquaredProbability.h"

#include "Math/VectorUtil.h"

#include "PhysicsTools/PatAlgos/plugins/PATSingleVertexSelector.h"

#include "CLHEP/Units/GlobalPhysicalConstants.h"

#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "PhysicsTools/PatUtils/interface/TriggerHelper.h"
#include "PhysicsTools/SelectorUtils/interface/Selector.h"

#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"
#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHitBuilder.h"
#include "TrackingTools/Records/interface/TransientRecHitRecord.h"

#include <TrackingTools/PatternTools/interface/TwoTrackMinimumDistance.h>
#include <TrackingTools/PatternTools/interface/ClosestApproachInRPhi.h>
#include <TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h>

#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"
#include "RecoVertex/TrimmedKalmanVertexFinder/interface/ConfigurableTrimmedVertexFinder.h"

#include "RecoTracker/TransientTrackingRecHit/interface/ProjectedRecHit2D.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TRecHit1DMomConstraint.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TRecHit2DPosConstraint.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TSiPixelRecHit.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TSiStripMatchedRecHit.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TSiStripRecHit1D.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TSiStripRecHit2DLocalPos.h"
#include "RecoTracker/TransientTrackingRecHit/interface/TkTransientTrackingRecHitBuilder.h"

#include <chrono>
#include <thread>

using pat::PATSingleVertexSelector;

using namespace std;
using namespace edm;
using namespace reco;
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class IOTest : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit IOTest(const edm::ParameterSet&);
      ~IOTest();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
 edm::EDGetToken tracks_, muons_, genParticles_;
 edm::EDGetToken hVtx_;
 edm::EDGetToken beamSpotHandle_;
 edm::EDGetToken trigger;

 TTree *Tree;
 double Pis_pt, Pis_eta, Pis_phi;
 double Pi_pt, Pi_eta, Pi_phi;
 double K_pt, K_eta, K_phi;
 double DS_pt, DS_eta, DS_phi;
 double D0_pt, D0_eta, D0_phi;
 double CL_vertex, sum_ptVertex2, sum_ptVertex;
 double x_p, y_p, z_p; 
 double x_s, y_s, z_s; 
 double L_abs, L_sigma;
 double cos_phi, pt_tracks;
 int vertex_size, num_tracks;
 bool passTrigger;


      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
IOTest::IOTest(const edm::ParameterSet& iConfig)

{
   edm::Service<TFileService> fs;
   tracks_= consumes<reco::TrackCollection>(edm::InputTag("generalTracks"));
   muons_= consumes<reco::TrackCollection>(edm::InputTag("standAloneMuons"));
   hVtx_= consumes<std::vector<reco::Vertex>>(edm::InputTag("offlinePrimaryVertices"));
   //genParticles_= consumes<edm::View<reco::GenParticle>>(edm::InputTag("genParticles"));
   //#PFJets
   //#GSF electron

}


IOTest::~IOTest()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
IOTest::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   edm::Handle<reco::TrackCollection> true_tracks;
   iEvent.getByToken(tracks_ , true_tracks );

   edm::Handle<reco::TrackCollection> muons;
   iEvent.getByToken(muons_ , muons );

   //edm::Handle<edm::View<reco::GenParticle> > genParticles;
   //iEvent.getByToken(genParticles_, genParticles);


   edm::Handle<std::vector<reco::Vertex>> hVtx;
   iEvent.getByToken(hVtx_ , hVtx);
   reco::Vertex primVertex;

   //for(size_t i = 0; i < genParticles->size(); ++ i) {
   //std::srand(std::time(0));
   //for(int i=0; i<2000; i++){
   //   atan(std::rand());
   //}
   //  const GenParticle & p= (*genParticles)[i];
   //  auto pt = p.pt();
   //  auto phi = p.phi();
   //  auto eta = p.eta();
 
//   }


   for (unsigned int t = 0; t < hVtx->size(); t++){
    auto primVertex = hVtx->at(t);
   for (std::vector<TrackBaseRef >::const_iterator tracks = primVertex.tracks_begin(); tracks != primVertex.tracks_end(); ++tracks) {
    const reco::Track *track = tracks->get();
    auto somma_ptVertex = track->pt();
    auto somma_etaVertex = track->eta();
    auto somma_phiVertex = track->phi();


   std::srand(std::time(0));
   for(int i=0; i<2000; i++){
      atan(std::rand());
   }

   if(!primVertex.isFake() && primVertex.isValid() && primVertex.ndof() > 4 && fabs(primVertex.z()) < 10 ){
    continue; 
   }

 }
  } 


   for (reco::TrackCollection::const_iterator track = muons->begin();  track != muons->end();  ++track) {
   std::srand(std::time(0));
   for(int i=0; i<2000; i++){
       atan(std::rand());
   }
    auto somma_ptVertex = track->pt();
    auto somma_etaVertex = track->eta();
    auto somma_phiVertex = track->phi();

	for (reco::TrackCollection::const_iterator track = true_tracks->begin();  track != true_tracks->end();  ++track) {
   std::srand(std::time(0));
   for(int i=0; i<2000; i++){
       atan(std::rand());
   }
    auto somma_ptVertex = track->pt();
    auto somma_etaVertex = track->eta();
    auto somma_phiVertex = track->phi();

   }
   }
}


// ------------ method called once each job just before starting event loop  ------------
void 
IOTest::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
IOTest::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
IOTest::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(IOTest);
