import ROOT

mesonGammaMass = ROOT.RooRealVar("mesonGammaMass","Phi+Photon invariant mass",100.,169.,"GeV")

fSignal = ROOT.TFile("Tfile/signal.root")
sig = fSignal.Get("myworkspace")

fBkg = ROOT.TFile("Tfile/exp_bkg.root")
bkg = fBkg.Get("myworkspace")

#fBkg = ROOT.TFile("che_bkg.root")
#bkg = fBkg.Get("myworkspace")

sigPDF = sig.pdf("sigPDF")
bkgPDF = bkg.pdf("expPDF")

lumi = ROOT.RooRealVar("lumi","luminosity",40*pow(10,15))
BR_phi= ROOT.RooRealVar("BR_phi","BR phi",0.49)
eff = ROOT.RooRealVar("eff","efficiency", 0.08)
cross = ROOT.RooRealVar("cross","cross section",48.6*pow(10,-12))
BR_H = ROOT.RooRealVar("BR_H","BR Higgs",0.000001,0.001)

Nbkg = ROOT.RooRealVar("Nbkg","Nbkg",586)
Nsig = ROOT.RooFormulaVar("Nsig","@0*@1*@2*@3*@4",ROOT.RooArgList(lumi,BR_phi,BR_H,eff,cross))

totPDF = ROOT.RooAddPdf("totPDF","tot pdf", ROOT.RooArgList(sigPDF,bkgPDF) , ROOT.RooArgList(Nsig,Nbkg))

ws_totPDF = ROOT.RooWorkspace("ws_totPDF")
getattr( ws_totPDF,'import')(totPDF)

fOut = ROOT.TFile("Tfile/tot_pdf.root","RECREATE")
ws_totPDF.Write()
ws_totPDF.Print()
fOut.Write()
fOut.Close()
