function results = im_crop_resize(im)

% Logo-removing Function
% Simplest way is to call this function in Matlab Image Bacth Processor APP
% Or else we shall define file bacth I/O programs

% IM      - Input image.
% RESULTS - The logo-removed GSV photos.

%img_size = size(im);
%The photos we collected using the script is 300*300;
%Crop into 300*275 will remove the logo perfectly

%from 300*300 to 256*256 while at the same time extract the logo
results = im(22:277,22:277,1:3);

%results = imcrop(im,[0 0 img_size(1) img_size(2)-25]);


%--------------------------------------------------------------------------
% img = imread('test.jpg');
% img
% results = im_crop_resize(img)
