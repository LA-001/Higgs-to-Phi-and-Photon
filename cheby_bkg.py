import ROOT

#open the file and get the histo
_file_Input = ROOT.TFile("histos_CR_BDTcat0_Sidebands.root")

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
c = ROOT.RooRealVar("c","c",0.,-10.,10.)
#d = ROOT.RooRealVar("d","d",0.,-10.,10.)
#e = ROOT.RooRealVar("e","e",0.,-10.,10.)
#f = ROOT.RooRealVar("f","f",0.,-10.,10.)
#g = ROOT.RooRealVar("g","g",0.,-10.,10.)

chePDF = ROOT.RooChebychev("chePDF","Chebychev",mesonGammaMass,ROOT.RooArgList(a,b,c))

#fit
f = chePDF.fitTo(d1,ROOT.RooFit.Range("left,right"),ROOT.RooFit.Save())

print "minNll = ", f.minNll()
print "2Delta_minNll = ", 2*(1910.80711016-f.minNll())


#Now plot the data points and the result
xplot = mesonGammaMass.frame(50)
d1.plotOn(xplot)
chePDF.plotOn(xplot)


print("chi^2 = ", xplot.chiSquare())

#Draw and save
canva = ROOT.TCanvas()
canva.cd()
xplot.Draw()
canva.SaveAs("Chebychev.png")

myworkspace = ROOT.RooWorkspace("myworkspace")
getattr( myworkspace,'import')(chePDF)

fOut = ROOT.TFile("che_bkg.root","RECREATE")
fOut.cd()
myworkspace.Write()
myworkspace.Print()
fOut.Close()
