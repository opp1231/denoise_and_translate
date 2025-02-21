path = getDirectory("home");
Dialog.create("Input Root");
	Dialog.addDirectory("Path to experiment root directory",path);
Dialog.show();

root = Dialog.getString();

i_ddir = root+"/rcan_output_test/";
o_ddir = root+"/denoised_bgsub_16bit/";

File.makeDirectory(o_ddir);

function bg_sub(input_dir, output_dir, fname){
	open(input_dir + fname);
	
	run("Subtract Background...", "rolling=50 stack");
	run("16-bit");
	saveAs("Tiff", output_dir + fname);
	close();
}

setBatchMode(true);
filelist = getFileList(i_ddir); 
for (i = 0; i < lengthOf(filelist); i++) {
    if (endsWith(filelist[i], ".tif")) { 
        bg_sub(i_ddir,o_ddir,filelist[i]);
    print("finished file " + i);
    }
}
setBatchMode(false);