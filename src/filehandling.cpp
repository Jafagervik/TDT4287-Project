#include "../include/filehandling.hpp"

void read_file(const std::string &filename)
{
    std::vector<std::string> dna_sequences;
    std::string line;
    std::ifstream file(filename);
    if (file.is_open())
    {
        while (getline(file, line))
        {
            dna_sequences.push_back(line);
        }
        file.close();
    }

    std::cout << "Number of sequences in file: " << dna_sequences.size() << "\n";
}

void write_file(const std::string_view &filename)
{
}
