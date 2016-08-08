
# coding: utf-8

# In[ ]:

import argparse 
import model
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def plot_data_matrix(data_matrix):
    pass


def main():
  
	# Define parser data
    parser = argparse.ArgumentParser(description='Plotting model data.')
    # First arguments. Models' Initial conditions (Months)
    parser.add_argument('--ic',dest='ini_con', metavar='months', type=str, nargs=1,		      help='Month of Initial condition ex. Jan Feb')    
    parser.add_argument('--lead',dest='leadtime', metavar='number', type=int, nargs=1,		      help='Leadtime in months (number)')
    # Specify models to exclude from command line
    parser.add_argument('--no-cfs', dest='cfs_bool', action="store_true", default= False, help="Don't display CFS V2 information")

    # Extract dates from args
    args=parser.parse_args()
    initialDate = args.ini_con[0]
    leadtime = args.leadtime[0]
    
    # Flow control depending on specified options
    if not args.cfs_bool:
        # Instantiate CFS and get datetime object
        cfsv2 = model.CFSV2(initialDate, leadtime)
        cfsv2.get_datetime_object()
        
        # Download files from ASCAT servers
        archivo = cfsv2.download_files()
    
        # Get figure handler and colormap
        m, cmap = model.generate_figure()   
        
        # Process 
        lat, lon, data = cfsv2.extract_data(archivo)
        model.plot_data(m, lon, lat, data, cmap)
        
        # Finalize plot design and show it
        plt.title('CFS - T2m')
        plt.show()

    else:
        print("You've discarded all models I know!")

if __name__ == "__main__":
    main()  

