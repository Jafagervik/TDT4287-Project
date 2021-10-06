#include "../include/filehandling.hpp"

std::vector<std::string> read_file(const std::string &filename)
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
    return dna_sequences;
}

std::unordered_map<uint16_t, uint16_t> vec_to_dict(std::vector<uint16_t> seqs)
{
    std::unordered_map<uint16_t, uint16_t> distribution;
    for (auto iter = seqs.begin(); iter != seqs.end(); ++iter)
    {
        // increment number of ocurences for a specific length of dna suffixes
        if (distribution.contains(*iter))
        {
            distribution[*iter]++;
        }
        distribution[*iter] = 1;
    }
    return distribution;
}

void write_dists_to_file(const std::string &filename, std::unordered_map<uint16_t, uint16_t> dists)
{
    std::string input;
    std::ofstream file(filename);

    if (file.is_open())
    {
        for (const auto &[key, value] : dists)
        {
            file << key << ' ' << value << '\n';
        }
        file.close();
    }
    std::cout << "Successfully wrote distributions to file!\n";
}
