import ROOT

#open the file and get the histo
_file_Input = ROOT.TFile("Tfile/histos_CR_BDTcat0_Sidebands.root")

#define the observable: meson+gamma invariant mass
mesonGammaMass = ROOT.RooRealVar("mesonGammaMass","Meson+Photon invariant mass",100.,169,"GeV")

mesonGammaMass.setRange("left",100.,120.)
mesonGammaMass.setRange("right",130.,169.)

#get the tree from the input file
tree_input = _file_Input.Get("tree_output")

#create from the tree the RooDataSet for the observable (called mesonGammaMass in the tree)
dataset = ROOT.RooDataSet("dataset","Signal dataset", ROOT.RooArgSet(mesonGammaMass), ROOT.RooFit.Import(tree_input))
d1 = dataset.reduce("mesonGammaMass<120. || mesonGammaMass>130.")
d1.Print("v")

#funzione da fittare
a = ROOT.RooRealVar("a","a",0.,-10.,10.)
b = ROOT.RooRealVar("b","b",0.,-10.,10.)

expPDF = ROOT.RooExponential("expPDF","Exponential",mesonGammaMass,a)

#fit
expPDF.fitTo(d1,ROOT.RooFit.Range("left,right"))

#Now plot the data points and the result
xplot = mesonGammaMass.frame(50)
d1.plotOn(xplot)
expPDF.plotOn(xplot)

#Draw and save
canva = ROOT.TCanvas()
canva.cd()
xplot.Draw()
canva.SaveAs("foto/exp_bkg.png")

myworkspace = ROOT.RooWorkspace("myworkspace")
getattr( myworkspace,'import')(expPDF)
getattr( myworkspace,'import')(d1)

fOut = ROOT.TFile("Tfile/exp_bkg.root","RECREATE")
fOut.cd()
myworkspace.Write()
myworkspace.Print()
fOut.Close()

