#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <dirent.h>
#include <errno.h>

//#define SHARED

struct __attribute__((__packed__)) wav_header_t
{
	char riff[4];
	uint32_t file_size;
	char wave_header[4];
	char format_chunk_marker[4];
	uint32_t length_of_format;
	uint16_t format_type;
	uint16_t channels;
	uint32_t sample_rate;
	uint32_t bytes_rate;
	uint16_t block_align;
	uint16_t bits_per_sample;
};

struct __attribute__((__packed__)) data_header_t
{
	char chunk_id[4];
	uint32_t size;
};

struct __attribute__((__packed__)) list_header_t
{
	char chunk_id[4];
	uint32_t size; //Size of the sub chunk
	char chunk_type[4];
};

//using the size_of_data_section and dividing by bytes_per_sample_per_channel

uint64_t get_num_samples_in_wave_file(char *directory, char *filename)
{
	size_t directory_length = strlen(directory);
	size_t filename_length = strlen(filename);
	char *filepath = NULL;
	if(directory[directory_length-1] != '/')
	{
		filepath = (char *)malloc(directory_length + filename_length + 1);
		strcpy(filepath, directory);
		*(filepath+directory_length) = '/';
		strcpy(filepath+directory_length+1, filename);
		*(filepath+directory_length+filename_length+1) = '\0';
	}
	else
	{
		filepath = (char *)malloc(directory_length + filename_length);	
		strcpy(filepath, directory);
		strcpy(filepath+directory_length, filename);
		*(filepath+directory_length+filename_length) = '\0';
	}


	struct wav_header_t wav_header;
	struct data_header_t data_header;

	FILE *fp;
	int retries = 0;
 	while((fp = fopen(filepath, "rb")) == NULL)
	{
		if(retries > 3){free(filepath);printf("[ERROR] errno: %d | error: %s\n", errno, strerror(errno));return 0;}
		else{retries++;}
	}
	free(filepath);
	fread(&wav_header, sizeof(struct wav_header_t), 1, fp);
	if(strncmp(wav_header.riff, "RIFF", 4) || strncmp(wav_header.wave_header, "WAVE", 4))
	{
		printf("[ERROR] RIFF segment: |%.4s| - WAVE segment: |%.4s|\n", wav_header.riff, wav_header.wave_header);
		fclose(fp);
		return 0;
	}
	fread(&data_header, sizeof(struct data_header_t), 1, fp);
	
	while(strncmp(data_header.chunk_id, "data", 4))
	{
		if(fseek(fp, data_header.size, SEEK_CUR))
		{
			printf("[ERROR] Not able to seek");
			fclose(fp);
			return 0;
		}
		fread(&data_header, sizeof(struct data_header_t), 1, fp);
	}
	fclose(fp);
	
	uint64_t sample_number = (8*data_header.size) / (wav_header.channels*wav_header.bits_per_sample);
	return sample_number;
}

char *get_filename_extension(char *filename, int *ext_length)
{
	*ext_length = 0;
	char *extension_position = NULL;
	char *current_position = filename;
	while(*current_position != '\0')
	{
		if(*current_position == '.')
		{
			extension_position = current_position;
			*ext_length = 0;
		}
		(*ext_length)++;
		current_position++;
	}
	(*ext_length)--;
	return extension_position; //This is optimal (Single pass over memory (best for cache))
}

uint64_t get_max_samples_in_wav_from_directory(char *directory)
{
	DIR *d;
	struct dirent *dir;

	uint64_t max_samples = 0;
	uint64_t file_count = 0;
	d = opendir(directory);
	if(d)
	{
		while((dir = readdir(d)) != NULL)
		{
			if(dir->d_type != DT_REG){continue;}
			int ext_length;
			char *filename_ext = get_filename_extension(dir->d_name, &ext_length);
			if(!filename_ext || ext_length!=3){continue;}
			if(!strncmp(".wav", filename_ext, 4))
			{
				file_count++;
				//We hit a wav file we think!
				uint64_t samples = get_num_samples_in_wave_file(directory, dir->d_name);
				max_samples = (samples > max_samples ? samples : max_samples);
			}
		}
	}
	return max_samples;
}

int main(int argc, char **argv)
{
	char *directory = "/home/oliver/Datasets/audioengine_single_word/clips";
	uint64_t num_samples_in_file;
	struct timespec start_time;
	struct timespec end_time;
	timespec_get(&start_time, TIME_UTC);

	num_samples_in_file = get_max_samples_in_wav_from_directory(directory);

	timespec_get(&end_time, TIME_UTC);

	uint64_t execution_time = pow(10,9)*(end_time.tv_sec - start_time.tv_sec) + (end_time.tv_nsec - start_time.tv_nsec);
	double execution_time_us = execution_time / 1000.0;
	printf("[INFO] Excecution time in microseconds: %.3f\n", execution_time_us);
	printf("[INFO] Number of samples: %ld\n", num_samples_in_file);
	return 0;
}
