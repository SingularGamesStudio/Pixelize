#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <vector>

#define x first
#define y second

using namespace std;

double ang(int x) {
    //return -pow(1.0 / 110.0, ((double)x) / 40.0) * 360 +360;
    return 360;
}

vector<int> enclose(const vector<int>& inp, int szx, int szy)
{
    const int maxdist = 100;
    int ** a = new int * [szx];
    int** ans = new int* [szx];
    int** used = new int* [szx];
    bool ** term = new bool* [szx];
    bool** done1 = new bool* [szx];
    pair<int, int> ** par = new pair<int, int>* [szx];
    for (int i = 0; i < szx; i++) {
        a[i] = new int[szy];
        ans[i] = new int[szy];
        done1[i] = new bool[szy];
        term[i] = new bool[szy];
        used[i] = new int[szy];
        par[i] = new pair<int, int>[szy];
        for (int j = 0; j < szy; j++) {
            a[i][j] = inp[i * szy + j];
            ans[i][j] = a[i][j];
            term[i][j] = 0;
            done1[i][j] = 0;
            used[i][j] = 0;
            par[i][j] = { 0, 0 };
        }
    }
    vector<pair<pair<int, int>, pair<int, int>>> edges;
    for (int i = 0; i < szx; i++) {
        for (int j = 0; j < szy; j++) {
            if (a[i][j]==10000) {
                pair<int, int> dir = { 0, 0 };
                bool ok = 0;
                for (int di = -1; di <= 1; di++) {
                    for (int dj = -1; dj <= 1; dj++) {
                        if (i + di >= 0 && i + di < szx && j + dj >= 0 && j + dj < szy && !(dj == 0 && di == 0) && a[i + di][j + dj] == 10000) {
                            if (dir == make_pair(0, 0)) {
                                dir = { di, dj };
                                ok = 1;
                            }
                            else ok = 0;
                        }
                    }
                }
                if (ok) {
                    term[i][j] = 1;
                    edges.push_back({ { i, j }, dir });
                }
            }
        }
    }
    random_shuffle(edges.begin(), edges.end());
    int num = 0;
    for (auto z : edges) {
        num++;
        pair<int, int> p0 = z.x;
        pair<int, int> dir = z.y;
        if (done1[p0.x][p0.y]) {
            continue;
        }
        deque<pair<int, int>> dots;
        used[p0.x][p0.y] = num;
        par[p0.x][p0.y] = {-1, -1};
        
        dots.push_back({ p0.x + 1, p0.y });
        dots.push_back({ p0.x + 1, p0.y+1 });
        dots.push_back({ p0.x + 1, p0.y-1 });
        dots.push_back({ p0.x - 1, p0.y });
        dots.push_back({ p0.x - 1, p0.y + 1 });
        dots.push_back({ p0.x - 1, p0.y - 1 });
        dots.push_back({ p0.x, p0.y + 1 });
        dots.push_back({ p0.x, p0.y - 1 });
        for (auto z1 : dots) {
            par[z1.x][z1.y] = p0;
            used[z1.x][z1.y] = num;
        }
        int k = 0;
        pair<int, int> ok = { -1, -1 };
        
        while (k<maxdist) {
            k++;
            dots.push_back({ -1, -1 });
            while (dots.front() != make_pair(-1, -1)) {
                pair<int, int> p = dots.front();
                dots.pop_front();
                double cosa = ((double)((p.x - p0.x) * dir.x + (p.y - p0.y) * dir.y)) / (sqrt((double)((p.x - p0.x) * (p.x - p0.x) + (p.y - p0.y) * (p.y - p0.y))) * sqrt((double)(dir.x * dir.x + dir.y * dir.y)));
                double alpha = acos(cosa);
                if (sqrt((double)((p.x - p0.x) * (p.x - p0.x) + (p.y - p0.y) * (p.y - p0.y))) <= k && alpha<=ang(k)) {
                    if (term[p.x][p.y]) {
                        ok = p;
                        break;
                    }
                    else {
                        int n_num = 0;
                        for (int di = -1; di <= 1; di++) {
                            for (int dj = -1; dj <= 1; dj++) {
                                if (p.x + di >= 0 && p.x + di < szx && p.y + dj >= 0 && p.y + dj < szy && !(dj == 0 && di == 0) && a[p.x + di][p.y + dj]>0 && a[p.x][p.y] < 10000) {
                                    n_num++;
                                    if (used[p.x + di][p.y + dj] < num) {
                                        used[p.x + di][p.y + dj] = num;
                                        par[p.x + di][p.y + dj] = p;
                                        dots.push_back({ p.x + di, p.y + dj });
                                    }
                                }
                            }
                        }
                        if (n_num == 1) {
                            for (int di = -2; di <= 2; di++) {
                                for (int dj = -2; dj <= 2; dj++) {
                                    if (p.x + di >= 0 && p.x + di < szx && p.y + dj >= 0 && p.y + dj < szy && !(dj == 0 && di == 0) && a[p.x + di][p.y + dj]>0 && a[p.x][p.y] < 10000 && used[p.x + di][p.y + dj] < num) {
                                        used[p.x + di][p.y + dj] = num;
                                        par[p.x + di][p.y + dj] = p;
                                        dots.push_back({ p.x + di, p.y + dj });
                                    }
                                }
                            }
                        }
                    }
                }
                else dots.push_back(p);
            }
            if (ok != make_pair(-1, -1))
                break;
            dots.pop_front();
        }
        if (ok != make_pair(-1, -1))
            done1[ok.x][ok.y] = 1;
        while (ok != make_pair(-1, -1)) {
            ans[ok.x][ok.y] = 5000;
            ok = par[ok.x][ok.y];
        }
        //return inp;
    }
    vector<int> res(szx * szy);
    for (int i = 0; i < szx; i++) {
        for (int j = 0; j < szy; j++) {
            if (ans[i][j] == 10000)
                res[i * szy + j] = 255;
            else if (ans[i][j] == 5000)
                res[i * szy + j] = 122;
            else res[i * szy + j] = 0;
        }
    }
    return res;
}



namespace py = pybind11;

py::array py_enclose(py::array_t<int, py::array::c_style | py::array::forcecast> array)
{
    vector<int> pos(array.size());
    memcpy(pos.data(), array.data(), array.size() * sizeof(int));

    //call function
    vector<int> result = enclose(pos, array.shape()[0], array.shape()[1]);
    //

    ssize_t              ndim = 2;//number of dimencions
    vector<ssize_t> shape = { array.shape()[0] , array.shape()[1] };//size of resulting vector
    vector<ssize_t> strides = { ((int)sizeof(int)) * array.shape()[1] , sizeof(int) };//...

    return py::array(py::buffer_info(
        result.data(),                           /* data as contiguous array  */
        sizeof(int),                          /* size of one scalar        */
        py::format_descriptor<int>::format(), /* data type                 */
        ndim,                                    /* number of dimensions      */
        shape,                                   /* shape of the matrix       */
        strides                                  /* strides for each axis     */
    ));
}

PYBIND11_MODULE(cpp, m) {
    m.def("enclose", &py_enclose);

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
