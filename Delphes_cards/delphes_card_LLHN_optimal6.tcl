#######################################
# Order of execution of various modules
#######################################

# Execution path includes both the original Isolation module and the new IsolationMuon module for debugging.
set ExecutionPath {
 ParticlePropagator

  ChargedHadronTrackingEfficiency
  ElectronTrackingEfficiency
  MuonTrackingEfficiency

  ChargedHadronMomentumSmearing
  ElectronMomentumSmearing
  MuonMomentumSmearing

  TrackMerger

  ECal
  HCal

  Calorimeter
  EFlowMerger
  EFlowFilter

  PhotonIsolation
  PhotonCaloIsolation
  PhotonEfficiency

  ElectronFilter
  ElectronIsolation
  ElectronCaloIsolation
  ElectronEfficiency

  ChargedHadronFilter

  MuonEfficiency

  MissingET

  NeutrinoFilter
  GenJetFinder
  GenMissingET

  FastJetFinder

  JetEnergyScale

  JetFlavorAssociation

  BTagging
  TauTagging
  
  #esta linea no es muy necesaria, habria que considerar que Isolation ya esta definido al llamarlo
  Isolation            ;# Original Isolation module
  IsolationMuon        ;# New IsolationMuon module for debugging

  TreeWriter
}

#################################
# Propagate particles in cylinder
#################################

module ParticlePropagator ParticlePropagator {
  set InputArray Delphes/stableParticles
  set OutputArray stableParticles
  set ChargedHadronOutputArray chargedHadrons
  set ElectronOutputArray electrons
  set MuonOutputArray muons

  # radius of the magnetic field coverage, in m
  set Radius 1.15
  # half-length of the magnetic field coverage, in m
  set HalfLength 3.512

  ## ATLAS ecal small measurements
  set RadiusMax 1.5
  set HalfLengthMax 3.512

  # magnetic field
  set Bz 2.0
}

####################################
# Charged hadron tracking efficiency
####################################

module Efficiency ChargedHadronTrackingEfficiency {
  set InputArray ParticlePropagator/chargedHadrons
  set OutputArray chargedHadrons

  # add EfficiencyFormula {efficiency formula as a function of eta and pt}
  # tracking efficiency formula for charged hadrons
  set EfficiencyFormula {
    (pt <= 0.1)   * (0.00) +
    (abs(eta) <= 1.5) * (pt > 0.1 && pt <= 1.0)   * (0.70) +
    (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.95) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1 && pt <= 1.0)   * (0.60) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.85) +
    (abs(eta) > 2.5)                                                  * (0.00)
  }
}

##############################
# Electron tracking efficiency
##############################

module Efficiency ElectronTrackingEfficiency {
  set InputArray ParticlePropagator/electrons
  set OutputArray electrons

  # tracking efficiency formula for electrons
  set EfficiencyFormula {
    (pt <= 0.1)   * (0.00) +
    (abs(eta) <= 1.5) * (pt > 0.1 && pt <= 1.0)   * (0.73) +
    (abs(eta) <= 1.5) * (pt > 1.0 && pt <= 1.0e2) * (0.95) +
    (abs(eta) <= 1.5) * (pt > 1.0e2)                * (0.99) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1 && pt <= 1.0)   * (0.50) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0 && pt <= 1.0e2) * (0.83) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0e2)                * (0.90) +
    (abs(eta) > 2.5)                                                  * (0.00)
  }
}

##########################
# Muon tracking efficiency
##########################

module Efficiency MuonTrackingEfficiency {
  set InputArray ParticlePropagator/muons
  set OutputArray muons

  # tracking efficiency formula for muons
  set EfficiencyFormula {
    (pt <= 0.1)   * (0.00) +
    (abs(eta) <= 1.5) * (pt > 0.1 && pt <= 1.0)   * (0.75) +
    (abs(eta) <= 1.5) * (pt > 1.0)                  * (0.99) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1 && pt <= 1.0)   * (0.70) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 1.0)                  * (0.98) +
    (abs(eta) > 2.5)                                                  * (0.00)
  }
}

########################################
# Momentum resolution for charged tracks
########################################

module MomentumSmearing ChargedHadronMomentumSmearing {
  set InputArray ChargedHadronTrackingEfficiency/chargedHadrons
  set OutputArray chargedHadrons

  # resolution formula for charged hadrons
  set ResolutionFormula {
    (abs(eta) <= 0.5) * (pt > 0.1) * sqrt(0.06^2 + pt^2*1.3e-3^2) +
    (abs(eta) > 0.5 && abs(eta) <= 1.5) * (pt > 0.1) * sqrt(0.10^2 + pt^2*1.7e-3^2) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1) * sqrt(0.25^2 + pt^2*3.1e-3^2)
  }
}

###################################
# Momentum resolution for electrons
###################################

module MomentumSmearing ElectronMomentumSmearing {
  set InputArray ElectronTrackingEfficiency/electrons
  set OutputArray electrons

  # resolution formula for electrons
  set ResolutionFormula {
    (abs(eta) <= 0.5) * (pt > 0.1) * sqrt(0.03^2 + pt^2*1.3e-3^2) +
    (abs(eta) > 0.5 && abs(eta) <= 1.5) * (pt > 0.1) * sqrt(0.05^2 + pt^2*1.7e-3^2) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1) * sqrt(0.15^2 + pt^2*3.1e-3^2)
  }
}

###############################
# Momentum resolution for muons
###############################

module MomentumSmearing MuonMomentumSmearing {
  set InputArray MuonTrackingEfficiency/muons
  set OutputArray muons

  # resolution formula for muons
  set ResolutionFormula {
    (abs(eta) <= 0.5) * (pt > 0.1) * sqrt(0.01^2 + pt^2*1.0e-4^2) +
    (abs(eta) > 0.5 && abs(eta) <= 1.5) * (pt > 0.1) * sqrt(0.015^2 + pt^2*1.5e-4^2) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 0.1) * sqrt(0.025^2 + pt^2*3.5e-4^2)
  }
}

##############
# Track merger
##############

module Merger TrackMerger {
  add InputArray ChargedHadronMomentumSmearing/chargedHadrons
  add InputArray ElectronMomentumSmearing/electrons
  add InputArray MuonMomentumSmearing/muons
  set OutputArray tracks
}

#############
#   ECAL
#############

module SimpleCalorimeter ECal {
  set ParticleInputArray ParticlePropagator/stableParticles
  set TrackInputArray TrackMerger/tracks

  set TowerOutputArray ecalTowers
  set EFlowTrackOutputArray eflowTracks
  set EFlowTowerOutputArray eflowPhotons

  set IsEcal true
  set EnergyMin 0.5
  set EnergySignificanceMin 2.0
  set SmearTowerCenter true

  # Bins and resolution settings
  set pi [expr {acos(-1)}]
  set PhiBins {}
  for {set i -180} {$i <= 180} {incr i} {
    add PhiBins [expr {$i * $pi/180.0}]
  }
  # 0.02 unit in eta up to eta = 1.5 (barrel)
  for {set i -85} {$i <= 86} {incr i} {
    set eta [expr {$i * 0.0174}]
    add EtaPhiBins $eta $PhiBins
  }
  # Endcaps resolution 1.5 < |eta| < 3.0
  set PhiBins {}
  for {set i -180} {$i <= 180} {incr i} {
    add PhiBins [expr {$i * $pi/180.0}]
  }
  for {set i 1} {$i <= 84} {incr i} {
    set eta [expr { -2.958 + $i * 0.0174}]
    add EtaPhiBins $eta $PhiBins
  }
  for {set i 1} {$i <= 84} {incr i} {
    set eta [expr { 1.4964 + $i * 0.0174}]
    add EtaPhiBins $eta $PhiBins
  }
  # CMS granularity for HF 3.0 < |eta| < 5.0
  set PhiBins {}
  for {set i -18} {$i <= 18} {incr i} {
    add PhiBins [expr {$i * $pi/18.0}]
  }
  foreach eta {-5 -4.7 -4.525 -4.35 -4.175 -4 -3.825 -3.65 -3.475 -3.3 -3.125 -2.958 3.125 3.3 3.475 3.65 3.825 4 4.175 4.35 4.525 4.7 5} {
    add EtaPhiBins $eta $PhiBins
  }
  # Energy fractions
  add EnergyFraction {0} {0.0}
  add EnergyFraction {11} {1.0}
  add EnergyFraction {22} {1.0}
  add EnergyFraction {111} {1.0}
  add EnergyFraction {12} {0.0}
  add EnergyFraction {13} {0.0}
  add EnergyFraction {14} {0.0}
  add EnergyFraction {16} {0.0}
  add EnergyFraction {1000022} {0.0}
  add EnergyFraction {1000023} {0.0}
  add EnergyFraction {1000025} {0.0}
  add EnergyFraction {1000035} {0.0}
  add EnergyFraction {1000045} {0.0}
  add EnergyFraction {9900012} {0.0}
  add EnergyFraction {9900014} {0.0}
  add EnergyFraction {9900016} {0.0}
  add EnergyFraction {310} {0.3}
  add EnergyFraction {3122} {0.3}
  # Resolution formula for ECAL
  set ResolutionFormula {
    (abs(eta) <= 3.2) * sqrt(energy^2*0.0017^2 + energy*0.101^2) +
    (abs(eta) > 3.2 && abs(eta) <= 4.9) * sqrt(energy^2*0.0350^2 + energy*0.285^2)
  }
}

#############
#   HCAL
#############

module SimpleCalorimeter HCal {
  set ParticleInputArray ParticlePropagator/stableParticles
  set TrackInputArray ECal/eflowTracks

  set TowerOutputArray hcalTowers
  set EFlowTrackOutputArray eflowTracks
  set EFlowTowerOutputArray eflowNeutralHadrons

  set IsEcal false
  set EnergyMin 1.0
  set EnergySignificanceMin 2.0
  set SmearTowerCenter true
  set pi [expr {acos(-1)}]

  # HCAL resolution settings
  set PhiBins {}
  for {set i -18} {$i <= 18} {incr i} {
    add PhiBins [expr {$i * $pi/18.0}]
  }
  foreach eta {-3.2 -2.5 -2.4 -2.3 -2.2 -2.1 -2 -1.9 -1.8 -1.7 -1.6 -1.5 -1.4 -1.3 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.1 2.2 2.3 2.4 2.5 2.6 3.3} {
    add EtaPhiBins $eta $PhiBins
  }
  # HCAL energy fractions
  add EnergyFraction {0} {1.0}
  add EnergyFraction {11} {0.0}
  add EnergyFraction {22} {0.0}
  add EnergyFraction {111} {0.0}
  add EnergyFraction {12} {0.0}
  add EnergyFraction {13} {0.0}
  add EnergyFraction {14} {0.0}
  add EnergyFraction {16} {0.0}
  add EnergyFraction {1000022} {0.0}
  add EnergyFraction {1000023} {0.0}
  add EnergyFraction {1000025} {0.0}
  add EnergyFraction {1000035} {0.0}
  add EnergyFraction {1000045} {0.0}
  add EnergyFraction {9900012} {0.0}
  add EnergyFraction {9900014} {0.0}
  add EnergyFraction {9900016} {0.0}
  add EnergyFraction {310} {0.7}
  add EnergyFraction {3122} {0.7}
  # Resolution formula for HCAL
  set ResolutionFormula {
    (abs(eta) <= 1.7) * sqrt(energy^2*0.0302^2 + energy*0.5205^2 + 1.59^2) +
    (abs(eta) > 1.7 && abs(eta) <= 3.2) * sqrt(energy^2*0.0500^2 + energy*0.706^2) +
    (abs(eta) > 3.2 && abs(eta) <= 4.9) * sqrt(energy^2*0.09420^2 + energy*1.00^2)
  }
}

#################
# Electron filter
#################

module PdgCodeFilter ElectronFilter {
  set InputArray HCal/eflowTracks
  set OutputArray electrons
  set Invert true
  add PdgCode {11}
  add PdgCode {-11}
}

######################
# ChargedHadronFilter
######################

module PdgCodeFilter ChargedHadronFilter {
  set InputArray HCal/eflowTracks
  set OutputArray chargedHadrons
  add PdgCode {11}
  add PdgCode {-11}
  add PdgCode {13}
  add PdgCode {-13}
}

###################################################
# Tower Merger (in case not using e-flow algorithm)
###################################################

module Merger Calorimeter {
  add InputArray ECal/ecalTowers
  add InputArray HCal/hcalTowers
  add InputArray MuonMomentumSmearing/muons
  set OutputArray towers
}

####################
# Energy flow merger
####################

module Merger EFlowMerger {
  add InputArray HCal/eflowTracks
  add InputArray ECal/eflowPhotons
  add InputArray HCal/eflowNeutralHadrons
  set OutputArray eflow
}

######################
# EFlowFilter
######################

module PdgCodeFilter EFlowFilter {
  set InputArray EFlowMerger/eflow
  set OutputArray eflow
  add PdgCode {11}
  add PdgCode {-11}
  add PdgCode {13}
  add PdgCode {-13}
}

##################
# Photon Track isolation
##################

module Isolation PhotonIsolation {
  set CandidateInputArray ECal/eflowPhotons
  set IsolationInputArray TrackMerger/tracks
  set OutputArray photons
  set DeltaRMax 0.2
  set PTMin 1.0
  set PTRatioMax 0.05
  set DeltaRMin 1e-05
  set UseMiniCone true
}

##################
# Photon Calorimeter isolation
##################

module Isolation PhotonCaloIsolation {
  set CandidateInputArray PhotonIsolation/photons
  set IsolationInputArray ECal/eflowTracks
  set IsolationInputArray ECal/eflowPhotons
  set OutputArray photons
  set DeltaRMax 0.2
  set PTMin 0.1
  set PTRatioMax 0.065
  set DeltaRMin 1e-05
  set UseMiniCone true
}

###################
# Photon efficiency
###################

module Efficiency PhotonEfficiency {
  set InputArray PhotonCaloIsolation/photons
  set OutputArray photons
  set EfficiencyFormula {
    (pt <= 10.0) * (0.00) +
    (abs(eta) <= 1.5) * (pt > 10.0)  * (1.00) +
    (abs(eta) > 1.5 && abs(eta) <= 2.37) * (pt > 10.0) * (1.00) +
    (abs(eta) > 2.37)                                  * (0.00)
  }
}

####################
# Electron track isolation
####################

module Isolation ElectronIsolation {
  set CandidateInputArray ElectronFilter/electrons
  set IsolationInputArray TrackMerger/tracks
  set OutputArray electrons
  set DeltaRMax 0.2
  set PTMin 1
  set PTRatioMax 0.15
  set DeltaRMin 0.01
  set UseMiniCone true
}

####################
# Electron Calorimeter isolation
####################

module Isolation ElectronCaloIsolation {
  set CandidateInputArray ElectronIsolation/electrons
  set IsolationInputArray ECal/eflowTracks
  set IsolationInputArray ECal/eflowPhotons
  set OutputArray electrons
  set DeltaRMax 0.2
  set PTMin 0.1
  set PTRatioMax 0.2
  set DeltaRMin 0.01
  set UseMiniCone true
}

#####################
# Electron efficiency
#####################

module Efficiency ElectronEfficiency {
  set InputArray ElectronCaloIsolation/electrons
  set OutputArray electrons
  set EfficiencyFormula {
    (pt <= 10.0) * (0.00) +
    (abs(eta) <= 1.5) * (pt > 10.0)  * (1.00) +
    (abs(eta) > 1.5 && abs(eta) <= 2.5) * (pt > 10.0)  * (1.00) +
    (abs(eta) > 2.5)                                   * (0.00)
  }
}

#################
# Muon efficiency
#################

module Efficiency MuonEfficiency {
  set InputArray MuonMomentumSmearing/muons
  set OutputArray muons
  set EfficiencyFormula {
    (pt <= 10.0) * (0.00) +
    (abs(eta) <= 1.5) * (pt > 10.0)  * (1.00) +
    (abs(eta) > 1.5 && abs(eta) <= 2.7) * (pt > 10.0)  * (1.00) +
    (abs(eta) > 2.7)                                   * (0.00)
  }
}

####################
# Missing ET merger
####################

module Merger MissingET {
  add InputArray Calorimeter/towers
  set MomentumOutputArray momentum
}

#####################
# Neutrino Filter
#####################

module PdgCodeFilter NeutrinoFilter {
  set InputArray Delphes/stableParticles
  set OutputArray filteredParticles
  set PTMin 0.0
  add PdgCode {12}
  add PdgCode {14}
  add PdgCode {16}
  add PdgCode {-12}
  add PdgCode {-14}
  add PdgCode {-16}
  add PdgCode {9900012}
  add PdgCode {9900014}
  add PdgCode {9900016}
}

#####################
# MC truth jet finder
#####################

module FastJetFinder GenJetFinder {
  set InputArray NeutrinoFilter/filteredParticles
  set OutputArray jets
  set JetAlgorithm 6
  set ParameterR 0.4
  set JetPTMin 25.0
}

#########################
# Gen Missing ET merger
########################

module Merger GenMissingET {
  add InputArray NeutrinoFilter/filteredParticles
  set MomentumOutputArray momentum
}

############
# Jet finder
############

module FastJetFinder FastJetFinder {
  set InputArray Calorimeter/towers
  set OutputArray jets
  set JetAlgorithm 6
  set ParameterR 0.4
  set JetPTMin 20.0
}

##################
# Jet Energy Scale
##################

module EnergyScale JetEnergyScale {
  set InputArray FastJetFinder/jets
  set OutputArray jets
  set ScaleFormula { sqrt( (3.0 - 0.2*(abs(eta)))^2 / pt + 1.0 ) }
}

########################
# Jet Flavor Association
########################

module JetFlavorAssociation JetFlavorAssociation {
  set PartonInputArray Delphes/partons
  set ParticleInputArray Delphes/allParticles
  set ParticleLHEFInputArray Delphes/allParticlesLHEF
  set JetInputArray JetEnergyScale/jets
  set DeltaR 0.5
  set PartonPTMin 1.0
  set PartonEtaMax 2.5
}

###########
# b-tagging
###########

module BTagging BTagging {
  set JetInputArray JetEnergyScale/jets
  set BitNumber 0
  add EfficiencyFormula {0} {0.002+7.3e-06*pt}
  add EfficiencyFormula {4} {0.20*tanh(0.02*pt)*(1/(1+0.0034*pt))}
  add EfficiencyFormula {5} {0.80*tanh(0.003*pt)*(30/(1+0.086*pt))}
}

#############
# tau-tagging
#############

module TrackCountingTauTagging TauTagging {
  set ParticleInputArray Delphes/allParticles
  set PartonInputArray Delphes/partons
  set TrackInputArray TrackMerger/tracks
  set JetInputArray JetEnergyScale/jets
  set DeltaR 0.2
  set DeltaRTrack 0.2
  set TrackPTMin 1.0
  set TauPTMin 1.0
  set TauEtaMax 2.5
  set BitNumber 0
  add EfficiencyFormula {1} {0.70}
  add EfficiencyFormula {2} {0.60}
  add EfficiencyFormula {-1} {0.02}
  add EfficiencyFormula {-2} {0.01}
}

#####################################################
# Find uniquely identified photons/electrons/tau/jets
#####################################################

# module UniqueObjectFinder UniqueObjectFinder {
#  add InputArray PhotonIsolation/photons photons
#  add InputArray ElectronIsolation/electrons electrons
#  add InputArray MuonEfficiency/muons muons
#  add InputArray JetEnergyScale/jets jets
# }

module Isolation Isolation_test {
  set CandidateInputArray TrackMerger/tracks
  set IsolationInputArray ECal/eflowTracks
  set IsolationInputArray ECal/eflowPhotons
  set OutputArray isolatedCandidates_test
  set DeltaRMax 0.2
  set PTMin 0.1
  set PTRatioMax 0.2
  set DeltaRMin 0.01
  set UseMiniCone true
}

##########################################
# New Debugging Module: IsolationMuon_test
##########################################

module IsolationMuon IsolationMuon_test {
  set CandidateInputArray TrackMerger/tracks
  set IsolationInputArray ECal/eflowTracks
  set IsolationInputArray ECal/eflowPhotons
  set OutputArray isolatedMuons_debug_test
  set DeltaRMax 0.2
  set PTMin 0.1
  set PTRatioMax 0.2
  set DeltaRMin 0.01
  set UseMiniCone true
}

##################
# ROOT Tree Writer
##################

module TreeWriter TreeWriter {
  # Original branches
  add Branch ECal/eflowTracks EFlowTrackECAL Track
  add Branch ECal/eflowPhotons EFlowPhoton Tower
  add Branch HCal/eflowTracks EFlowTrack Track
  add Branch HCal/eflowNeutralHadrons EFlowNeutralHadron Tower
  add Branch PhotonEfficiency/photons Photon Photon
  add Branch ElectronEfficiency/electrons Electron Electron
  add Branch JetEnergyScale/jets Jet Jet
  add Branch MuonEfficiency/muons Muon Muon  
  add Branch MissingET/momentum MissingET MissingET

  # New test branches for debugging isolation results
  add Branch Isolation_test/isolatedCandidates_test IsolatedCandidateTest Candidate
  add Branch IsolationMuon_test/isolatedMuons_debug_test IsolatedMuonDebugTest Candidate
}
