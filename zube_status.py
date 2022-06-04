import copy



class ZubeStatus:

    def __init__(self, ph,pv,pm):
        self.point_h = ph
        self.point_v = pv
        self.point_m = pm
        self.id = 0
    @staticmethod
    def copy(originate):
        status = ZubeStatus(
            copy.deepcopy(originate.point_h),
            copy.deepcopy(originate.point_v),
            copy.deepcopy(originate.point_m))
        status.id = originate.id
        return status

    @staticmethod
    def equal(a,b):
        if a[0] != b[0]:
            return False
        return a[1] == b[1]

    @staticmethod
    def arry_overlap(a,b):
        for posa in a:
            for posb in b:
                if ZubeStatus.equal(posa,posb):
                    return True


    def overlap(self, b):
        if ZubeStatus.arry_overlap(self.point_h,b.point_h):
            return True
        if ZubeStatus.arry_overlap(self.point_v,b.point_v):
            return True
        if ZubeStatus.arry_overlap(self.point_m,b.point_m):
            return True
        return False



#
# class ZubeStatusList:
