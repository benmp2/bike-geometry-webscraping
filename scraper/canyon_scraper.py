from .base_scraper import base_scraper
import pandas as pd

class canyon_geometry_scraper(base_scraper):

    def __init__(self, site_url):
        
        super().__init__(site_url)

        self.comp_titles ='geometryTable__titleInner'
        self.header = 'geometryTable__headingData'
        self.size_data = 'geometryTable__sizeData'
        self.frame_geom_image = 'detailedGeometry__img js-geometryImgSvg'
    
    def bike_frame_sizes(self):
        
        frame_sizes = self.soup.find_all(attrs={'class':self.header})
        header = [x.text.strip().split()[0] for x in frame_sizes]
        header = sorted(set(header), key=header.index)
        
        return header
    
    def bike_geometry_comps(self):
        
        geometry_comps = self.soup.find_all(attrs={'class':self.comp_titles})
        rows = [' '.join(x.text.strip().split()) for x in geometry_comps]
        
        return rows
    
    def geometry_comp_sizedata(self):
    
        input_tags = self.soup.find_all(attrs={'class':self.size_data})
        data = [el.text for el in input_tags]
        return data

    def chunk_sizedata(self,data,frame_sizes):

        offset = len(frame_sizes)
        data = [data[i:i + offset] for i in range(0, len(data), offset)]

        return data
    
    def generate_df(self):
        geom_entries = self.bike_geometry_comps()
        frame_sizes = self.bike_frame_sizes()
        data = self.geometry_comp_sizedata()
        chunked_data = self.chunk_sizedata(data,frame_sizes)
        
        return pd.DataFrame(data=chunked_data,index=geom_entries,columns = frame_sizes)
    
    def get_frame_geom_img_url(self):
        
        img_links = self.soup.find_all(attrs={'class': self.frame_geom_image})
        return img_links[0].attrs['data']