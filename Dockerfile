FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Clone your repository
RUN git clone --branch v1.2 --single-branch https://github.com/NSAPH-Data-Processing/zip2zcta_master_xwalk.git . 

# Update the base environment
RUN mamba env update -n base -f requirements.yml 
#&& mamba clean -a

# Create symlinks to data placeholders
RUN python src/create_data_symlinks.py

CMD ["snakemake", "--cores", "1"]
