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

BR_H_num = ROOT.RooRealVar("BR_H_num","BR Higgs for shape",pow(10,-4))

scale_factor = ROOT.RooRealVar("scale_factor","scale factor",(3*pow(10,18))/(40*pow(10,15)))

Nbkg = ROOT.RooFormulaVar("Nbkg","@0*586",scale_factor)
Nsig = ROOT.RooFormulaVar("Nsig","@0*@1*@2*@3*@4*@5",ROOT.RooArgList(lumi,BR_phi,BR_H,eff,cross,scale_factor))
Nsig_shape = ROOT.RooFormulaVar("Nsig_shape","@0*@1*@2*@3*@4*@5",ROOT.RooArgList(lumi,BR_phi,BR_H_num,eff,cross,scale_factor))

totPDF = ROOT.RooAddPdf("totPDF","tot pdf", ROOT.RooArgList(sigPDF,bkgPDF) , ROOT.RooArgList(Nsig,Nbkg))

eventi_sig = Nsig_shape.getVal()
eventi_bkg = Nbkg.getVal()
print(eventi_sig)
print(eventi_bkg)

totPDF_shape = ROOT.RooAddPdf("totPDF_shape","tot pdf shape", ROOT.RooArgList(sigPDF,bkgPDF) , ROOT.RooArgList(Nsig_shape,Nbkg))

xplot = mesonGammaMass.frame(50)
totPDF_shape.plotOn(xplot)

canva = ROOT.TCanvas("Tot" , "Tot function" , 800 , 500)
canva.cd()
xplot.Draw()
#canva.SaveAs("foto/tot_3ab.png")

#generate
data = totPDF_shape.generate(ROOT.RooArgSet(mesonGammaMass),eventi_bkg+eventi_sig)
data.SetName("data")

xplot_gen = mesonGammaMass.frame(50)
data.plotOn(xplot_gen)
totPDF_shape.plotOn(xplot_gen)

canva_gen = ROOT.TCanvas("generate" , "tot function - generate" , 800 , 500)
canva_gen.cd()
xplot_gen.Draw()
#canva_gen.SaveAs("foto/tot_gen_3ab.png")

ws_tot = ROOT.RooWorkspace("ws_tot")
getattr( ws_tot,'import')(data)
getattr( ws_tot,'import')(totPDF)

fOut = ROOT.TFile("Tfile/tot_pdf.root","RECREATE")
ws_tot.Write()
ws_tot.Print()
fOut.Write()
fOut.Close()
