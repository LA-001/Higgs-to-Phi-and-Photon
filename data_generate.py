import ROOT

fPDF = ROOT.TFile("Tfile/tot_pdf.root")
f = fPDF.Get("ws_totPDF")

totPDF = f.pdf("totPDF")
mesonGammaMass = f.var("mesonGammaMass")

f.var("BR_H").setVal(pow(10 ,-4))

scale_factor = ROOT.RooRealVar("scale_factor","scale factor",(3*pow(10,18))/(40*pow(10,15)))

#generate
data = totPDF.generate(ROOT.RooArgSet(mesonGammaMass),(594)*scale_factor.getVal())
data.SetName("data")

xplot_gen = mesonGammaMass.frame(50)
data.plotOn(xplot_gen)

canva_gen = ROOT.TCanvas("generate" , "tot function - generate" , 800 , 500)
canva_gen.cd()
xplot_gen.Draw()
canva_gen.SaveAs("foto/data_gen_40fb.png")

ws_data = ROOT.RooWorkspace("ws_data")
getattr( ws_data,'import')(data)
getattr( ws_data,'import')(scale_factor)

fOut = ROOT.TFile("Tfile/data_gen.root","RECREATE")
ws_data.Write()
ws_data.Print()
fOut.Write()
fOut.Close()
