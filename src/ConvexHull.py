import numpy as np
# bagi dua area pada dataset, dengan mencari titik yang memiliki jarak paling jauh
# fungsi ini menghasilkan dua himpunan S1 dan S2
# S1 kumpulan titik yang berada di bagian kiri
# S2 kumpulan titik uang berada di bagian kanan 

def bagi_dua(start, end, points):
    # apabila ukuran data tidak sesuai 
    if points is None or points.shape[0] < 1:
        return None, None
    S1, S2 = [], []

    # menentukan apakah sebuah titik berada di sebelah kiri garis pembagi 
    # atau disebelah kanan garis pembagi
    for _, point in enumerate(points):
        dis = posisi_titik(start, end, point)
        if dis > 0:
            S1.append(point)
        else:
            S2.append(point)
    S1 = np.vstack(S1) if len(S1) else None
    S2 = np.vstack(S2) if len(S2) else None
    return S1, S2

# menentukan apakah sebuah titik terdapat disebelah kanan atau kiri dari garis pembagi
# dengan menghitung cross product nya 
def posisi_titik(start, end, point, epsilon = 1e-8):

   return np.cross(end - start, point-start)/(np.linalg.norm(end-start)+epsilon) 

# fungsi untuk membagi daerah sisa menjadi S1.1 dan S1.2 
# kemudian S2.1 dan S2.2
def pembagian_segitiga(points, P, C, Q):
    if points is None:
        return None, None
    
    S1, S2 = [], []

    for _, point in enumerate(points):
        disPC = posisi_titik(P, C, point)
        disCQ = posisi_titik(C, Q, point)
        if disPC > 0 and disCQ < 0:
            S1.append(point)
        elif disPC < 0 and disCQ > 0:
            S2.append(point)
    
    S1 = np.vstack(S1) if len(S1) else None
    S2 = np.vstack(S2) if len(S2) else None

    return S1, S2


# fungsi untuk memilih titik yang membuat sudut paling besar
# apabila terdapat titik yang memiliki jarak yang sama terhadap
# garis pembagi

def sudut_terbesar(x):
    x0, y0 = x[:,0].mean(), x[:,1].mean()
    theta = np.arctan2(x[:,1] - y0, x[:,0] - x0)
    index = np.argsort(theta)
    x = x[index]

    return x

#pembuatan kelas myConvexHull

class myConvexHull:

    # class myConvexHull memiliki dua atribut, yaitu points dan array yang berisi points yang merupakan convex_hull
    def __init__(self):
        self.points = None
        self.convex_hull = []

    def __call__(self, point_set):
        return self.forward(point_set)

    def reset(self):
        self.points = None
        self.convex_hull = []

    def forward(self, point_set):
        if point_set is None or len(point_set) < 3:
            return None
        self.reset()
        self.points = np.unique(point_set, axis=0)
        return self.quickHull()

    def findHull(self, points, P, Q):
        if points is None:
            return None
        distance = 0.0
        C, index = None, None
        for i, point in enumerate(points):
            distance_1 = abs(posisi_titik(P,Q,point))
            if distance_1 > distance:
                C = point
                index = i
                distance = distance_1
        if C is not None:
            self.convex_hull.append(C)
            # point yang sudah dimasukkan kedalam array convex hull, maka point tersebut akan dihapus dari 
            # array point tersebut
            points = np.delete(points, index, axis=0)
        else: 
            return
        
        S1, S2 = pembagian_segitiga(points, P, C, Q)
        self.findHull(S1, P, C)
        self.findHull(S2, C, Q)

    def quickHull(self):
        # mengurutkan points 
        self.points = self.points[np.lexsort(np.transpose(self.points)[::-1])]

        # mencari point paling kiri dan point paling kanan
        point_paling_kiri, point_paling_kanan = self.points[0], self.points[-1]

        self.points = self.points[1:-1] # mendapatkan sisa dari points
        self.convex_hull.append(point_paling_kiri) # point paling kiri sudah pasti merupakan point convex hull
        self.convex_hull.append(point_paling_kanan) # point paling kiri sudah pasti merupakan point convex hull

        self.points_kanan, self.points_kiri = bagi_dua(start=point_paling_kiri,end=point_paling_kanan, points = self.points)

        self.findHull(self.points_kanan, point_paling_kiri, point_paling_kanan)
        self.findHull(self.points_kiri, point_paling_kanan, point_paling_kiri)

        self.convex_hull = np.stack(self.convex_hull)
        self.convex_hull = sudut_terbesar(self.convex_hull)

        if self.convex_hull.shape[0] >= 3:
            return self.convex_hull
    

