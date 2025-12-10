import pandas as pd
import geopandas as gpd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib import patches, colors
import matplotlib.patches as mpatches
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.patheffects as pe

## Misc functions


# Administrative boundaries
lake = gpd.read_file('/Users/david/Dropbox/PhD/GitHub/COVID19/Data/Mapping/lake.geojson')
lake.NOM = ['Lake Geneva', '', '']
cantons = gpd.read_file(
    '/Users/david/Dropbox/PhD/Data/Databases/SITG/SHAPEFILE_LV95_LN02/swissBOUNDARIES3D_1_3_TLM_KANTONSGEBIET.shp')
communes = gpd.read_file(
    '/Users/david/Dropbox/PhD/Data/Databases/SITG/SHAPEFILE_LV95_LN02/swissBOUNDARIES3D_1_3_TLM_HOHEITSGEBIET.shp')
communes = communes[communes.KANTONSNUM == 25]
communes = communes.to_crs(2056)

def show_values(axs, orient="v", digits=2, fontsize=8, space=0.05):
    """
    Display the values on top of or next to the bars in a bar plot.

    Parameters:
    axs (matplotlib Axes or ndarray of Axes): The axes object(s) containing the bar plot.
    orient (str, optional): Orientation of the values. 'v' for vertical (on top of the bars),
                            'h' for horizontal (next to the bars). Default is 'v'.
    digits (int, optional): Number of digits to display for the values. Default is 2.
    fontsize (int, optional): Font size for the displayed values. Default is 8.
    space (float, optional): Space between the bars and the displayed values in case of 'h' orientation.
                             Default is 0.05.

    Returns:
    None

    Examples:
    1. Single Axes object:
       show_values(ax, orient='v', digits=2, fontsize=8, space=0.05)

    2. ndarray of Axes objects:
       show_values(axs, orient='h', digits=1, fontsize=10, space=0.1)
    """

    def _single(ax):
        """
        Display values for a single Axes object.

        Parameters:
        ax (matplotlib Axes): The axes object containing the bar plot.

        Returns:
        None
        """
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height() * 0.02)
                value = '{:.{}f}'.format(p.get_height(), digits)
                ax.text(_x, _y, value, size=fontsize, ha="center")
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height() * 0.5)
                value = '{:.{}f}'.format(p.get_width(), digits)
                ax.text(_x, _y, value, size=fontsize, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

def update_variable_names(summary_table, variable_names, table_type):
    name_mapper = variable_names.set_index('old')['new'].to_dict()
    if table_type == 'summary':
        name_mapper = {f"{key}, mean (SD)": f"{value}, mean (SD)" for key, value in name_mapper.items()}
    if table_type == 'prevalence':
        name_mapper = {f"{key}, n (%)": f"{value}, n (%)" for key, value in name_mapper.items()}

    summary_table = summary_table.rename(index=name_mapper)
    return summary_table

def translate_cat(col, lang):
    translate_dict = {
        'FR': {
            'Nouveau point chaud': 'New hot spot',
            'Point chaud consécutif': 'Consecutive hot spot',
            'Intensification de point chaud': 'Intensifying hot spot',
            'Point chaud persistant': 'Persistent hot spot',
            'Point chaud diminuant': 'Diminishing hot spot',
            'Point chaud sporadique': 'Sporadic hot spot',
            'Point chaud oscillant': 'Oscillating hot spot',
            'Point chaud historique': 'Historical hot spot',
            'Nouveau point froid': 'New cold spot',
            'Point froid consécutif': 'Consecutive cold spot',
            'Intensification de point froid': 'Intensifying cold spot',
            'Point froid persistant': 'Persistent cold spot',
            'Point froid diminuant': 'Diminishing cold spot',
            'Point froid sporadique': 'Sporadic cold spot',
            'Point froid oscillant': 'Oscillating cold spot',
            'Point froid historique': 'Historical cold spot',
            'Aucun modèle détecté': 'No pattern detected',
        },
        'EN': {
            'Nouveau point chaud': 'New hot spot',
            'Point chaud consécutif': 'Consecutive hot spot',
            'Intensification de point chaud': 'Intensifying hot spot',
            'Point chaud persistant': 'Persistent hot spot',
            'Point chaud diminuant': 'Diminishing hot spot',
            'Point chaud sporadique': 'Sporadic hot spot',
            'Point chaud oscillant': 'Oscillating hot spot',
            'Point chaud historique': 'Historical hot spot',
            'Nouveau point froid': 'New cold spot',
            'Point froid consécutif': 'Consecutive cold spot',
            'Intensification de point froid': 'Intensifying cold spot',
            'Point froid persistant': 'Persistent cold spot',
            'Point froid diminuant': 'Diminishing cold spot',
            'Point froid sporadique': 'Sporadic cold spot',
            'Point froid oscillant': 'Oscillating cold spot',
            'Point froid historique': 'Historical cold spot',
            'Aucun modèle détecté': 'No pattern detected',
        }
    }
    col = col.map(translate_dict[lang])
    return col

def get_consecutive(lst, max_time):
    consec_lsts = []
    for k, g in groupby(enumerate(lst), lambda ix : ix[0] - ix[1]):
        consecutive_list = list(map(itemgetter(1), g))
#         print(consecutive_list)
        consec_lsts.append(consecutive_list)
#         print(len(consec_lsts))
        if len(consec_lsts) > 1:
            return np.nan
        else:
            if max_time in consecutive_list and len(consecutive_list)>1:
                
                return consecutive_list
            else:
                return np.nan

colors_cl_getis_en = {
'New cold spot': '#eff3ff',
'Decreasing cold spot': "#80cdc1",
'Persistent cold spot': '#313695',
'Historical cold spot': '#2166ac',
'Sporadic cold spot': '#67a9cf',
'Oscillating cold spot': '#d1e5f0',
'Cold spot intensification': '#c51b8a',
'Persistent hot spot': '#e41a1c',
'Historical hot spot': '#b2182b',
'Sporadic hot spot': '#ef8a62',
'Oscillating hot spot': '#fddbc7',
'Hot spot intensification': '#e7298a',
'New hot spot': '#ffeda0',
'Decreasing hot spot': "#fb9a99",
'No pattern detected': '#f0f0f0'
}

def masked_emergent_getis(gdf, gdf_centre, category, dict_cl, labels):
    fig, ax = plt.subplots(figsize=(12, 12))

    mask_quadrant = ~(gdf['class'] == category)
    non_quadrant = gdf[mask_quadrant]
    df_quadrant = gdf[~mask_quadrant]
    union2 = df_quadrant.unary_union.boundary
    communes.plot(color = 'lightgrey', ax = ax, zorder = 1)
    # communes.boundary.plot(color = 'black', linewidth=0.2, ax = ax, zorder = 1)
    # Add Geneva city boundary and annotation
    # geneva_city = communes[communes.NAME == 'Genève']
    # geneva_city.boundary.plot(ax=ax, color='black', linewidth=0.8, zorder = 3)
    communes_to_map = gpd.sjoin(communes, df_quadrant[['geometry']], predicate='intersects', how = 'left')
    communes_to_map = communes_to_map[communes_to_map.nbid.isnull()==False]
    communes_to_map.boundary.plot(ax=ax, color='black', linewidth=0.6, zorder = 5)
    # communes_to_map.apply(lambda x: ax.annotate(text=x.NAME, xy=x.geometry.centroid.coords[0], ha='center', size=10, alpha = 0.6, zorder=7), axis=1)
    communes_to_map.loc[communes_to_map.NAME == 'Genève','NAME'] = 'Geneva'
    communes_to_map.apply(lambda x: ax.annotate(text=x.NAME, 
                                               xy=x.geometry.centroid.coords[0],
                                               ha='center',
                                               size=7,
                                               zorder=99,
                                               path_effects=[
                                                   pe.withStroke(linewidth=2, foreground='white')
                                               ]),
                          axis=1)

    # Add Geneva city label at centroid
    # centroid = geneva_city.geometry.centroid.iloc[0]
    # ax.annotate('Geneva', xy=(centroid.x, centroid.y), fontsize=12, fontweight='bold', 
    #             ha='center', va='center', zorder = 5)
    lake.plot(color = 'lightblue',ax = ax, zorder = 7)
    lake.apply(lambda x: ax.annotate(text=x.NOM, xy=x.geometry.centroid.coords[0], ha='center', size=12, alpha = 0.8, zorder=8), axis=1)

    hmap = colors.ListedColormap([dict_cl[i] for i in gdf['class'].sort_values().unique()])
    y = gdf['class'] + ' [' + gdf['class'].map(gdf['class'].value_counts()).astype(str) + ']'
    with warnings.catch_warnings():  # temorarily surpress geopandas warning
        warnings.filterwarnings('ignore', category=UserWarning)
        gdf.plot(y, linewidth = 0.01, cmap = hmap, ax=ax, alpha=1, zorder=1, legend = False)
        non_quadrant.plot(color = 'white',alpha = 0.9,linewidth=0, zorder = 4, ax = ax)
    gpd.GeoSeries([union2]).plot(linewidth=0.3, ax=ax, color='black', zorder = 4)
    gdf_centre.plot(c = '#31a354', markersize = 40, alpha = 0.8, marker = 'x', ax = ax, zorder = 6)
    ax.set_axis_off()
    custom_patch = [mpatches.Patch(color=dict_cl[category], label=labels[category])]
    custom_patch.append(plt.Line2D([0], [0], marker='x', color='#31a354', linestyle='None', 
                                 markersize=10, markeredgewidth=3, label='Breast screening centers'))
    # Create the custom legend with the patch
    ax.legend(handles=custom_patch, title='Categories - N women (%)', fontsize=10, title_fontsize = 12, loc='upper left')
    # Add screening centers to legend


    scalebar = ScaleBar(1, units="m", location="lower right")
    ax.add_artist(scalebar)
    # ax.set_title(category, size = 16)
    return fig, ax

def pca_map(X,PC_a, PC_b, figsize=(10,10), sup="", print_values= False):
    #PCA
    columns=X.columns.values
    pca=PCA(n_components=8)
    pca.fit(X)
    pca_values=pca.components_
    
    #Plot
    plt.figure(figsize=figsize)
    plt.rcParams.update({'font.size': 14}) 
    
    #Plot circle
    x=np.linspace(start=-1,stop=1,num=500)
    y_positive=lambda x: np.sqrt(1-x**2) 
    y_negative=lambda x: -np.sqrt(1-x**2)
    plt.plot(x,list(map(y_positive, x)), color='maroon')
    plt.plot(x,list(map(y_negative, x)),color='maroon')
    
    #Plot smaller circle
    x=np.linspace(start=-0.5,stop=0.5,num=500)
    y_positive=lambda x: np.sqrt(0.5**2-x**2) 
    y_negative=lambda x: -np.sqrt(0.5**2-x**2)
    plt.plot(x,list(map(y_positive, x)), color='maroon')
    plt.plot(x,list(map(y_negative, x)),color='maroon')
    
    #Create broken lines
    x=np.linspace(start=-1,stop=1,num=30)
    plt.scatter(x,[0]*len(x), marker='_',color='maroon')
    plt.scatter([0]*len(x), x, marker='|',color='maroon')

    #Define color list
    colors = ['blue', 'red', 'green', 'black', 'purple', 'brown']
    if len(pca_values[0]) > 6:
        colors=colors*(int(len(pca_values[0])/6)+1)

    #Plot arrow
    add_string=""
    for i in range(len(pca_values[0])):
        xi=pca_values[PC_a-1][i]
        yi=pca_values[PC_b-1][i]
        plt.arrow(0,0, 
                  dx=xi, dy=yi, 
                  head_width=0.03, head_length=0.03, 
                  color=colors[i], length_includes_head=True)
        if print_values==True:
            add_string=f" ({round(xi,2)} {round(yi,2)})"
        plt.text(pca_values[PC_a-1, i], 
                 pca_values[PC_b-1, i] , 
                 s=columns[i] + add_string )

    plt.xlabel(f"Component {PC_a} ({round(pca.explained_variance_ratio_[PC_a-1]*100,2)}%)")
    plt.ylabel(f"Component {PC_b} ({round(pca.explained_variance_ratio_[PC_b-1]*100,2)}%)")
    plt.title('Variable factor map (PCA)')
    plt.suptitle(sup, y=1, fontsize=18)
    plt.show()

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']), size = 3)
def abline(slope, intercept):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--', c = 'lightblue')
def avline(slope, intercept):
    axes = plt.gca()
    y_vals = np.array(axes.get_ylim())
    x_vals = intercept + slope * y_vals
    plt.plot(x_vals, y_vals, '--', c = 'lightblue')

def plot_hc(clusters,df,col,period):
    fig, ax = plt.subplots(1, figsize=(15, 15))
    hmap = colors.ListedColormap(['#2166ac','#67a9cf','#d1e5f0','#b2182b','#ef8a62','#fddbc7','#f7f7f7'])
    communes.plot(ax = ax, label='Communes',alpha = 0.3,color=None,edgecolor='black',facecolor='grey')
    communes.apply(lambda x: ax.annotate(text=x.NAME, xy=x.geometry.centroid.coords[0], ha='center',size = 7),axis=1);
    
    lake.plot(ax = ax, label='Lake',alpha = 1,color = 'lightblue',edgecolor='None')
#     df.plot(col,cmap=hmap,markersize = 3,alpha = 0.4,ax = ax,categorical=True)
    hmap = colors.ListedColormap(['#beaed4','#fdc086','#7fc97f'])
    ##plot
    df_high = df[df[col].isin(['1 High-High','4 High-Low'])]
    df_low = df[df[col].isin(['3 Low-Low','2 Low-High'])]

    df_low.plot('gp_hc',cmap = hmap,ax = ax,alpha = 1,categorical = True,edgecolor='blue',linewidth=0.2)
    df_high.plot('gp_hc',cmap = hmap,ax = ax,alpha = 1,categorical = True,edgecolor='red',linewidth=0.2)

#     chulls_cold.plot(ax = ax,color = 'blue',alpha = 0.4,edgecolor='None')
#     hmap = colors.ListedColormap(['#fdbf6f','#cab2d6', '#ffffb3','#f03b20'])
#     ashapes_hc_hot.plot('gp_hc',cmap = hmap,ax = ax,alpha = 0.6,categorical = True,edgecolor='red',linewidth=1.4)
#     chulls_hot.plot(ax = ax,color = 'red',alpha = 0.4,edgecolor='None')
#     ashapes_hc_cold.apply(lambda x: ax.annotate(text=x['desc'], xy=x.geometry.centroid.coords[0], ha='center',size = 8),axis=1);
#     ashapes_hc_hot.apply(lambda x: ax.annotate(text=x['desc'], xy=x.geometry.centroid.coords[0], ha='center',size = 8),axis=1);

    ax.set_facecolor('grey')
    ax.set_axis_off()
    filename = "Getis Clusters Alpha Shapes with HC - {} - {}.pdf".format('HA - Mammo',period)
    plt.title(period)
    plt.savefig(cluster_result_folder/filename, dpi = 300,bbox_inches = 'tight')
    return fig, ax

def render_mpl_table(data, col_width=3.0, row_height=0.5, font_size=12,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size, dpi = 180)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax