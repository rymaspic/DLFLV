function results = logo_crop(im)

% Logo-removing Function
% Simplest way is to call this function in Matlab Image Bacth Processor APP
% Or else we shall define file bacth I/O programs

% IM      - Input image.
% RESULTS - The logo-removed GSV photos.

img_size = size(im);
%The photos we collected using the script is 300*300;
%Crop into 300*275 will remove the logo perfectly

results = im(22:278,22:278,3);

%results = imcrop(im,[0 0 img_size(1) img_size(2)-25]);


%--------------------------------------------------------------------------
