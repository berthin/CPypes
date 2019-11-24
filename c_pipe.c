// To compile use -O0 , need to doble check why the code crashes for
// other optimizations

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

#include <fcntl.h>
#include <unistd.h>

#include <sys/stat.h>
#include <sys/types.h>


#define MAX 1005
const char* FIFO = "/tmp/myfifo";

void run_fifo(void)
{
    // file descriptor
    int fd = 0;
    mkfifo(FIFO, 0666);

	static char output[MAX];
	char* input;
	size_t sz_input;

	while (getline(&input, &sz_input, stdin) != -1)
    {
		fd = open(FIFO, O_WRONLY);
		write(fd, input, strlen(input) + 1);
		close(fd);

        fd = open(FIFO, O_RDONLY);
        read(fd, output, sizeof(output));
		if (strlen(output) > 0)
		{
			printf("%s", output);
		}
        close(fd);
    }
}

int main()
{
    run_fifo();
    return 0;
}
