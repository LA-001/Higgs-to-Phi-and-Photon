import ROOT

#open the file and get the histo
_file_Input = ROOT.TFile("Tfile/histos_SR_BDTcat0_SignalggH.root")

#define the observable: meson+gamma invariant mass
mesonGammaMass = ROOT.RooRealVar("mesonGammaMass","Meson+Photon invariant mass",100.,169.,"GeV")

#get the tree from the input file
tree_input = _file_Input.Get("tree_output")

#create from the tree the RooDataSet for the observable (called mesonGammaMass in the tree)
dataset = ROOT.RooDataSet("dataset","Signal dataset", ROOT.RooArgSet(mesonGammaMass), ROOT.RooFit.Import(tree_input))

#define a lineshape to fit
#try with a gaussian, so we need to define the mean and the sigma
mean = ROOT.RooRealVar("mean","Gaussian mean",125.,121.,129.)
sigma_L = ROOT.RooRealVar("sigma_L","CB sigma left", 1., 0.001, 3.)
sigma_R = ROOT.RooRealVar("sigma_R","CB sigma right",1., 0.00001, 3.)
alpha_L= ROOT.RooRealVar("alpha_L","CB alphs left",2.,0.001,5.)
n_L = ROOT.RooRealVar("n_L","CB n left",2.,0.001,5.)
alpha_R = ROOT.RooRealVar("alpha_R","CB alphs right",2.,0.001,5.)
n_R = ROOT.RooRealVar("n_R","CB n right",4.,0.001,8.)

sigPDF = ROOT.RooCrystalBall("sigPDF","The signal PDF",mesonGammaMass,mean, sigma_L, sigma_R, alpha_L, n_L, alpha_R, n_R)

#now try to fit
sigPDF.fitTo(dataset)

#Now plot the data points and the result
xplot = mesonGammaMass.frame(50)
dataset.plotOn(xplot)
sigPDF.plotOn(xplot)

#Draw and save
canva = ROOT.TCanvas("CB" , "CB function" , 800 , 500)
canva.cd()
xplot.Draw()
canva.SaveAs("foto/fit_signal.png")

myworkspace = ROOT.RooWorkspace("myworkspace")
getattr(myworkspace,'import')(sigPDF)

fOut = ROOT.TFile("Tfile/signal.root","RECREATE")
fOut.cd()
myworkspace.Write()
myworkspace.Print()
fOut.Close()
