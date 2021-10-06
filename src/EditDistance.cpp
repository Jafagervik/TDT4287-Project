#include "../include/EditDistance.hpp"

matrix edit_distance(const std::string &A, const std::string &B) {
    uint16_t m = A.size() - 1;
    uint16_t n = B.size() - 1;

    using matrix = std::vector<std::vector<uint16_t>>;

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

    return memo;
}

uint16_t backtrack(const matrix &M, const std::string_view &A, const std::string_view &B) {
    uint16_t r = M.size() - 1;
    uint16_t c = M[0].size() - 1;

    while (r > 0 && c > 0) {
    }
}

bool allow_mismatch(const matrix &M, const float &mismatch_percentage) {
}