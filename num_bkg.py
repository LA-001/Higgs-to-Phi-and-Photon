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

num = dataset.numEntries()

dataset.Print("num")
