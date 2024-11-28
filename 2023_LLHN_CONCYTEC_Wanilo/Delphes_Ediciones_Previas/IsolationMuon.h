/*
 *  Delphes: a framework for fast simulation of a generic collider experiment
 *  Copyright (C) 2012-2014  Universite catholique de Louvain (UCL), Belgium
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef IsolationMuon_h
#define IsolationMuon_h

/** \class IsolationMuon
 *
 *  Isolation module specifically configured for muon isolation.
 *  Sums transverse momenta of isolation objects (tracks, calorimeter towers, etc)
 *  within a DeltaR cone around a muon candidate and calculates the fraction of this sum
 *  to the candidate's transverse momentum. Outputs candidates that have
 *  the transverse momenta fraction within (PTRatioMin, PTRatioMax].
 *
 *  \author Adapted by [Your Name] - based on Isolation module
 *
 */

#include "classes/DelphesModule.h"

class TObjArray;
class ExRootFilter;
class IsolationMuonClassifier; // Updated name to avoid conflict

class IsolationMuon: public DelphesModule
{
public:
  IsolationMuon();
  ~IsolationMuon();

  void Init();
  void Process();
  void Finish();

private:
  Double_t fDeltaRMax;           // Maximum DeltaR for isolation cone
  Double_t fPTRatioMax;          // Maximum transverse momentum ratio for isolation
  Double_t fPTSumMax;            // Maximum allowed sum of transverse momenta in cone
  Double_t fDeltaRMin;           // Minimum DeltaR for isolation cone if using minicone approach
  Bool_t fUsePTSum;              // Flag to use sum of PT instead of ratio
  Bool_t fUseRhoCorrection;      // Flag to apply rho correction
  Bool_t fUseMiniCone;           // Flag to use minicone approach for isolation

  IsolationMuonClassifier *fClassifier; // Updated name for classifier
  ExRootFilter *fFilter;                // Filter to apply isolation cuts

  TIterator *fItIsolationInputArray;    // Iterator for isolation input array
  TIterator *fItCandidateInputArray;    // Iterator for candidate input array
  TIterator *fItRhoInputArray;          // Iterator for rho input array

  const TObjArray *fIsolationInputArray; // Array of particles used for isolation calculation
  const TObjArray *fCandidateInputArray; // Array of candidate muons to test for isolation
  const TObjArray *fRhoInputArray;       // Array of rho values for pile-up correction

  TObjArray *fOutputArray;               // Output array of isolated candidates

  ClassDef(IsolationMuon, 1)
};

#endif
