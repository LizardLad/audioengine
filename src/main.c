#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

struct wav_header_struct
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
	char data_chunk_header[4];
	uint32_t data_size;
};

//using the size_of_data_section and dividing by bytes_per_sample_per_channel

int main(int argc, char **argv)
{
	char *filename = "test.wav";
	char buffer[44];
	FILE *fp = fopen(filename, "rb");
	fread(buffer, 44, 1, fp);
	fclose(fp);
	struct wav_header_struct *header = (struct wav_header_struct *)buffer;
	uint64_t num_samples_in_file = (8 * header->data_size) / (header->bits_per_sample);
	printf("%ld\n", num_samples_in_file);
	printf("Data size: %d\n", header->data_size);
	printf("Number of channels: %d\n", header->channels);
	printf("Filename: %s\n", filename);
	printf("Data chunk header: %c%c%c%c\n", header->data_chunk_header[0],
		       	header->data_chunk_header[1], header->data_chunk_header[2],
		       	header->data_chunk_header[3]);
	printf("Bytes per sample: %d\n", header->bits_per_sample / 8);
	printf("Audio Format idx: %d\n", header->format_type);
	return 0;
}
