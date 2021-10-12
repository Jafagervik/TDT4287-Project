#include "../include/EditDistance.hpp"

auto edit_distance(const std::string &A, const std::string &B) {
    uint16_t m = A.size() - 1;
    uint16_t n = B.size() - 1;

    matrix memo(m, std::vector<uint16_t>(n, 0));

    for (int r = 0; r < m; ++r)
        memo[r][0] = r;

    for (int c = 0; c < n; ++c)
        memo[0][c] = c;

    uint16_t cost;

    for (int r = 1; r < m; ++r) {
        for (int c = 1; c < n; ++c) {
            cost = A[r - 1] == B[c - 1] ? 1 : 0;
            memo[r][c] == std::min((uint16_t)(memo[r - 1][c - 1] + cost), memo[r][c - 1], memo[r - 1][c]);
        }
    }

    return memo, memo[m - 1][n - 1];
}

void backtrack(const matrix &memo, const std::string_view A, const std::string_view B) {
    // TODO: Add some math to this
    uint16_t m = A.size() - 1;
    uint16_t n = B.size() - 1;

    uint16_t i = m - 1;
    uint16_t j = n - 1;

    while (i > 0 && j > 0) {
        if (A[i - 1] == B[j - 1]) {
            std::cout << "\\";
            i -= 1;
            j -= 1;
        } else if (memo[i][j - 1] > memo[i - 1][j]) {
            std::cout << "--";
            j -= 1;
        } else {
            std::cout << "|";
            i -= 1;
        }
    }

    if (i == 0) {
        for (uint16_t a = 0; a < j; ++a)
            std::cout << "--";
    }

    if (j == 0) {
        for (uint16_t b = 0; b < i; ++b)
            std::cout << "--";
    }
}

bool allow_mismatch(const uint16_t &ed, const uint16_t &num_of_mismatches, const float &mismatch_percentage) {
    return true ? true : false;
}