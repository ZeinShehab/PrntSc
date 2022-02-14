# ABOUT
PrintSc is a python script that scrapes random images from the prntsc website. It uses geckodriver and selenium as the main tools

---

# USAGE
- `python3 prnt.py <n_images> <check_duplicates>` where `<n_images>` is the number of images you would like to download and `check_duplicates` is an optional paremeter and if passed `True` will prevent the script from downloading the same image twice

- Make sure to have geckodriver installed and added to the PATH if you're on windows or added to /usr/bin if you are on linux

- The exclude folder contains images that you would like to exclude from your search. By default it contains some uninteresting images

- The blacklist text file contains urls that lead to an excluded image (there might be multiple urls that lead to the same image) and these urls in the blacklist file are also excluded from the search

- The images folder is the folder where the images will be downloaded to