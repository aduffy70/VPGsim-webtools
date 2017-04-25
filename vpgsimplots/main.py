#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from urllib import urlopen


class MainHandler(webapp.RequestHandler):
    def get(self):
        region = self.request.get('region')
        urls = self.get_plot_urls(region)
        self.response.out.write('<html><body>')
        if urls[0] == 0:
            self.response.out.write("""
                <p>No demographics data found. Are you sure you are logging data?</p>
                """)
        else:
            self.response.out.write("""
                <p><img src="%s" border="1"/></p>
                """ % urls[0])
        if urls[1] == 0:
            self.response.out.write("""
                <p>No allele frequency or heterozygosity data found. Are you sure you are logging data?</p>
                """)
        else:
            self.response.out.write("""
                <p><img src="%s" border="1"/></p>
                <p><img src="%s" border="1"/></p>
                """ % (urls[1], urls[2]))
        self.response.out.write('</body></html>')

    def get_plot_urls(self, region_name):
        """
        Returns a list of the 3 google charts urls of plots for a region.
        """
        plot_size = '600x300'
        plot_urls = [0,0,0]
        # Read the demographics file into lists for each lifestage and find the max value
        try:
            dem_file_name = 'http://129.123.16.10/vpgsim-logs/local-%s-demographics.log' % region_name
            dem_file = urlopen(dem_file_name, 'r')
            time_data = []
            spore_data = []
            gametophyte_data = []
            sporophyte_data = []
            max_data_value = 0
            for line in dem_file:
                data = line.strip().split(',')
                if int(data[1]) > max_data_value:
                    max_data_value = int(data[1])
                if int(data[2]) > max_data_value:
                    max_data_value = int(data[2])
                if int(data[3]) > max_data_value:
                    max_data_value = int(data[3])
                time_data.append(data[0])
                spore_data.append(data[1])
                gametophyte_data.append(data[2])
                sporophyte_data.append(data[3])
            max_time = int(time_data[-1])
            min_time = int(time_data[0])
            dem_file.close()
        except:
            plot_urls[0] = 0
        else:
            # Only submit 50 timepoints to google charts.
            time_step = (max_time / 50) + 1
            start_index = max_time % time_step

            # Make strings from these reduced datasets
            time_data_string = ','.join(time_data[start_index::time_step])
            spore_data_string = ','.join(spore_data[start_index::time_step])
            gametophyte_data_string = ','.join(gametophyte_data[start_index::time_step])
            sporophyte_data_string = ','.join(sporophyte_data[start_index::time_step])

            # Generate the url string
            dem_url_string = 'http://chart.apis.google.com/chart'
            dem_url_string += '?chxr=%s,%s,%s|%s,%s,%s' % (0, start_index, max_time,
                                                       1, 0, max_data_value)
            dem_url_string += '&chxs=%s,%s,%s,%s,%s,%s|%s,%s,%s,%s,%s,%s' % (0, 676767, 11.5,
                           0, 'lt', 676767, 1, 676767, 11.5, 0.5, 'lt', 676767)
            dem_url_string += '&chxt=x,y'
            dem_url_string += '&chs=%s' % plot_size
            dem_url_string += '&cht=lxy'
            dem_url_string += '&chco=000000,FF9900,0000FF'
            dem_url_string += '&chds=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                           start_index, max_time, 0, max_data_value,
                           start_index, max_time, 0, max_data_value,
                           start_index, max_time, 0, max_data_value)
            dem_url_string += '&chd=t:%s|%s|%s|%s|%s|%s' % (
                           time_data_string, spore_data_string,
                           time_data_string, gametophyte_data_string,
                           time_data_string, sporophyte_data_string)
            dem_url_string += '&chdl=Spores|Gametophytes|Sporophytes'
            dem_url_string += '&chdlp=b'
            dem_url_string += '&chls=1,4,1|1,10,5|1,3,3'
            dem_url_string += '&chma=5,5,5,25'
            dem_url_string += '&chtt=Population+Demographics'
            plot_urls[0] = dem_url_string

        # Read the allele frequency and hwe file into lists
        try:
            hwe_file_name = 'http://129.123.16.10/vpgsim-logs/local-%s-hwe.log' % region_name
            hwe_file = urlopen(hwe_file_name, 'r')
            time_data = []
            freq_data5 = []
            freq_data4 = []
            freq_data3 = []
            freq_data2 = []
            freq_data1 = []
            hwe_data5 = []
            hwe_data4 = []
            hwe_data3 = []
            hwe_data2 = []
            hwe_data1 = []
            for line in hwe_file:
                data = line.strip().split(',')
                time_data.append(data[0])
                if data[1] != 'NA':
                    freq_data5.append(data[1])
                    hwe_data5.append(data[2])
                    freq_data4.append(data[3])
                    hwe_data4.append(data[4])
                    freq_data3.append(data[5])
                    hwe_data3.append(data[6])
                    freq_data2.append(data[7])
                    hwe_data2.append(data[8])
                    freq_data1.append(data[9])
                    hwe_data1.append(data[10])
                else:
                    freq_data5.append('_')
                    hwe_data5.append('_')
                    freq_data4.append('_')
                    hwe_data4.append('_')
                    freq_data3.append('_')
                    hwe_data3.append('_')
                    freq_data2.append('_')
                    hwe_data2.append('_')
                    freq_data1.append('_')
                    hwe_data1.append('_')
            max_time = int(time_data[-1])
            min_time = int(time_data[0])
            hwe_file.close()
        except:
            plot_urls[1] = 0
            plot_urls[2] = 0
        else:
            # Only submit 25 timepoints to google charts.
            time_step = (max_time / 25) + 1
            start_index = max_time % time_step

            # Make strings from these reduced datasets
            time_data_string = ','.join(time_data[start_index::time_step])
            freq_data5_string = ','.join(freq_data5[start_index::time_step])
            hwe_data5_string = ','.join(hwe_data5[start_index::time_step])
            freq_data4_string = ','.join(freq_data4[start_index::time_step])
            hwe_data4_string = ','.join(hwe_data4[start_index::time_step])
            freq_data3_string = ','.join(freq_data3[start_index::time_step])
            hwe_data3_string = ','.join(hwe_data3[start_index::time_step])
            freq_data2_string = ','.join(freq_data2[start_index::time_step])
            hwe_data2_string = ','.join(hwe_data2[start_index::time_step])
            freq_data1_string = ','.join(freq_data1[start_index::time_step])
            hwe_data1_string = ','.join(hwe_data1[start_index::time_step])

            # Generate the allele frequency url string
            freq_url_string = 'http://chart.apis.google.com/chart'
            freq_url_string += '?chxr=%s,%s,%s|%s,%s,%s' % (0, start_index, max_time,
                                                       1, 0, 1)
            freq_url_string += '&chxs=%s,%s,%s,%s,%s,%s|%s,%s,%s,%s,%s,%s' % (0, 676767, 11.5,
                           0, 'lt', 676767, 1, 676767, 11.5, 0.5, 'lt', 676767)
            freq_url_string += '&chxt=x,y'
            freq_url_string += '&chs=%s' % plot_size
            freq_url_string += '&cht=lxy'
            freq_url_string += '&chco=000000,FF9900,0000FF,FF0000,00FFFF'
            freq_url_string += '&chds=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1)
            freq_url_string += '&chd=t:%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
                           time_data_string, freq_data5_string,
                           time_data_string, freq_data4_string,
                           time_data_string, freq_data3_string,
                           time_data_string, freq_data2_string,
                           time_data_string, freq_data1_string)
            freq_url_string += '&chdl=Locus5|Locus4|Locus3|Locus2|Locus1'
            freq_url_string += '&chdlp=b'
            freq_url_string += '&chls=1,4,1|1,10,5|1,3,3|1,5,5|1,5,2'
            freq_url_string += '&chma=5,5,5,25'
            freq_url_string += '&chtt=Allele+Frequencies'

            plot_urls[1] = freq_url_string

            # Generate the hwe url string
            hwe_url_string = 'http://chart.apis.google.com/chart'
            hwe_url_string += '?chxr=%s,%s,%s|%s,%s,%s' % (0, start_index, max_time,
                                                       1, 0, 1)
            hwe_url_string += '&chxs=%s,%s,%s,%s,%s,%s|%s,%s,%s,%s,%s,%s' % (0, 676767, 11.5,
                           0, 'lt', 676767, 1, 676767, 11.5, 0.5, 'lt', 676767)
            hwe_url_string += '&chxt=x,y'
            hwe_url_string += '&chs=%s' % plot_size
            hwe_url_string += '&cht=lxy'
            hwe_url_string += '&chco=000000,FF9900,0000FF,FF0000,00FFFF'
            hwe_url_string += '&chds=%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1,
                           start_index, max_time, 0, 1)
            hwe_url_string += '&chd=t:%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
                           time_data_string, hwe_data5_string,
                           time_data_string, hwe_data4_string,
                           time_data_string, hwe_data3_string,
                           time_data_string, hwe_data2_string,
                           time_data_string, hwe_data1_string)
            hwe_url_string += '&chdl=Locus5|Locus4|Locus3|Locus2|Locus1'
            hwe_url_string += '&chdlp=b'
            hwe_url_string += '&chls=1,4,1|1,10,5|1,3,3|1,5,5|1,5,2'
            hwe_url_string += '&chma=5,5,5,25'
            hwe_url_string += '&chtt=Observed+Heterozygosity'

            plot_urls[2] = hwe_url_string
        return plot_urls

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
