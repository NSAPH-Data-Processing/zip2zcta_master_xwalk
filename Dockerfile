FROM condaforge/mambaforge:23.3.1-1

# install build essentials
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

# Clone your repository
RUN git clone --branch v1.3 --single-branch https://github.com/NSAPH-Data-Processing/zip2zcta_master_xwalk.git . 

# Update the base environment
RUN mamba env update -n base -f requirements.yml 
#&& mamba clean -a

# Create symlinks to data placeholders
RUN python src/create_dir_paths.py

# Copy configuration inside container
RUN mkdir -p "/opt/local/app/"
COPY app.config.yaml data/metadata/* /opt/local/app/

CMD ["snakemake", "--cores", "1"]
