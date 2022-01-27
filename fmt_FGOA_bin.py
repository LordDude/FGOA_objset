from inc_noesis import *


def registerNoesisTypes():
	handle = noesis.register("Fate Grand Order Arcade", "_obj.bin")
	noesis.setHandlerTypeCheck(handle, noepyCheckType)
	noesis.setHandlerLoadModel(handle, noepyLoadModel)
	return 1


def noepyCheckType(data):
	if len(data) < 8:
		return 0
	# else:
	# 	return 1
	bs = NoeBitStream(data)

	if bs.readInt() != int(84288768):
		return 0
	else:
		return 1

class BoneClass:
    def __init__(self) -> None:
        self.BoneID = int()
        self.Name = str()
        self.Mat = None
        self.ParentID = int()

class ObjData:
    def __init__(self) -> None:
        self.UNK4LOC = int()
        self.UNK4Count = int()
        self.AttribLOC = int()
        self.VLOC = int()
        self.FLOC = int()
        self.SubCount = int()
        self.MatC = int()
        self.Mats = int()
        self.SkelLOC = int()
        self.BoneMap = int()
        self.Bone25 = int()
        self.StringC = int()
        self.StringLOC = int()
        self.MorphDC = int()
        self.MorphData = int()
        self.MorphC = int()
        self.MorphNames = int()

class Attribs:
    def __init__(self) -> None:
        self.VertexPush = int()
        self.VertexCount = int()
        self.FacePush = int()
        self.FaceCount = int()
        self.UNKInt = []
        self.UNKF = []
        self.BoneMapCount = int()
        self.BoneMapPush = int()

class UNK4Data:
    def __init__(self) -> None:
        self.UNKID = int()
        self.UNK1 = int()
        self.UNK2 = int()
        self.DataType = int()
        self.VStride = int()
        self.VTest = float()
        self.UTest = float()
        self.US = float()
        self.VS = float()
        self.UNKFloat = float()
        self.MorphCount = int()

class Morph:
    def __init__(self) -> None:
        self.Name = str()
        self.Pad = int()
        self.UNK4ID = int()
        self.Count = int()
        self.Pad2 = int()

class Material:
    def __init__(self) -> None:
        self.Name = str()
        self.UNK1 = int()
        self.UNK2 = int()
        self.UNK3 = int()
        self.UNK4 = int()
        self.UNK5 = int()
        self.UNKF1 = float()
        self.UNKF2 = float()
        self.UNK6 = int()
        self.UNK7 = int()
        self.UNKF3 = float()
        self.UNKF4 = float()
        self.UNKF5 = float()
        self.UNKF6 = float()
        self.UNK8 = int()
        self.UNKF7 = float()
        self.UNKF8 = float()
        self.UNKF9 = float()
        self.UNKF10 = float()
        self.UNKF11 = float()
        self.UNKF12 = float()
        self.UNKF13 = float()

class Bone25:
    def __init__(self) -> None:
        self.Mat43 = bytes()
        self.Name = str()
        self.Parent = int()

def GetNames(bs, LOC, C):
    Names = []
    bs.seek(LOC)
    for Z in range(0, C):
        M = bs.readInt64()
        B = bs.tell()
        bs.seek(M)
        Names.append(bs.readString())
        bs.seek(B)
    return Names

def GetUNK4(bs, LOC, Count) -> UNK4Data:
    bs.seek(LOC)
    UNK4List = []
    for X in range(0, Count):
        #Size 80
        U = UNK4Data()
        U.UNKID = bs.readInt()
        bs.seek(8, 1)
        U.UseCount = bs.readInt()
        U.UNK2 = bs.readInt64()
        U.DataType = bs.readInt()
        U.VStride = bs.readInt()
        U.VTest = bs.readUShort()
        U.UTest = bs.readUShort()
        #print(bs.tell())
        U.US = bs.readFloat()
        U.VS = bs.readFloat()
        U.UNKFloat = bs.readFloat()
        bs.seek(12, 1)
        U.MorphCount = bs.readInt()
        bs.seek(16, 1)
        UNK4List.append(U)
        # print(U.__dict__)
    return UNK4List

def GetAttrib(bs, LOC, Count) -> Attribs():
    AList = []
    bs.seek(LOC)
    for Q in range(0, Count):
        #Size 208
        A = Attribs()
        Blank = bs.readInt()
        VertexPush = bs.readInt()
        FaceCount = bs.readInt()
        FacePush = bs.readInt()
        VertexCount = bs.readInt()
        A.UNKInt = bs.read(2*'I')
        # H1 = bs.readUShort()
        # H2 = bs.readUShort()
        # H3 = bs.readUShort()
        # H4 = bs.readUShort()
        F3 = bs.readFloat()
        F4 = bs.readFloat()
        F1 = bs.readFloat()
        F2 = bs.readFloat()
        # A.UNKF = [H1, H2, H3, H4, F1, F2]
        bs.seek(48, 1)
        A.BoneMapCount = bs.readInt()
        A.BoneMapPush = bs.readInt()
        bs.seek(36,1)
        F5 = bs.readFloat()
        F6 = bs.readFloat()
        F7 = bs.readFloat()
        F8 = bs.readFloat()
        bs.seek(56,1)
        A.VertexCount = VertexCount
        A.VertexPush = VertexPush
        A.FaceCount = FaceCount
        A.FacePush = FacePush
        A.UNKF = [F3, F4, F1, F2, F5, F6, F7, F8]
        AList.append(A)
        # print(A.__dict__)
    return AList
#39
def GetStrings(bs, LOC, Count):
    Strings = []
    bs.seek(LOC)
    for S in range(0, Count):
        SC = bs.readShort()
        Strings.append(bs.readString())
        # print(Strings[S])
    return Strings
#16
def GetMaterials(bs, LOC, Count, St) -> Material():
    Materials = []
    bs.seek(LOC)
    #print(LOC, Count)
    for S in range(0, Count):
        M = Material()
        #print(bs.tell())
        M.Name = St[bs.readUInt64()]
        bs.seek(16, 1)
        M.UNK1 = bs.readInt()
        M.UNK2 = bs.readInt()
        M.UNK3 = bs.readInt()
        M.UNK4 = bs.readInt()
        M.UNK5 = bs.readInt()
        M.UNKF1 = bs.readFloat()
        M.UNKF2 = bs.readFloat()
        M.UNK6 = bs.readInt64()
        M.UNK7 = bs.readInt()
        M.UNKF3 = bs.readFloat()
        M.UNKF4 = bs.readFloat()
        M.UNKF5 = bs.readFloat()
        M.UNKF6 = bs.readFloat()
        M.UNK8 = bs.readInt()
        M.UNKF7 = bs.readFloat()
        M.UNKF8 = bs.readFloat()
        M.UNKF9 = bs.readFloat()
        M.UNKF10 = bs.readFloat()
        M.UNKF11 = bs.readFloat()
        M.UNKF12 = bs.readFloat()
        M.UNKF13 = bs.readFloat()
        bs.seek(72, 1)
        Materials.append(M)
    return Materials
#22
def GetTextureList(bs, LOC, St):
    Test2 = []
    bs.seek(LOC)
    UNK1 = bs.readUInt64()+80
    UNK2 = bs.readUInt64()+80
    Count = bs.readUInt64()
    bs.seek(UNK2)
    for T2 in range(0, Count):
        Test2.append(St[bs.readInt64()])
        bs.seek(16, 1)
        print(Test2[T2])
    return Test2

def GetUNK25(bs, LOC, Plus, St):
    Bone25List = []
    Bone25Remap = []
    boneMatrixList = []
    boneInvMatrixList = []
    bs.seek(LOC)
    POS0 = bs.readInt64()
    POS1 = bs.readInt64()
    POS2 = bs.readInt64()
    POS3 = bs.readInt64()
    POS4 = bs.readInt64()
    Count0 = bs.readInt()
    Count1 = bs.readInt()
    Count2 = bs.readInt()
    Count3 = bs.readInt()
    bs.seek(POS0+Plus)
    BoneNames = []
    Dups = []
    for u in range(0, Count0):
        m01, m02, m03, m04 = bs.read("4f")
        m11, m12, m13, m14 = bs.read("4f")
        m21, m22, m23, m24 = bs.read("4f")
        boneMtx = NoeMat43([NoeVec3((m01, m02, m03)), NoeVec3((m11, m12, m13)), NoeVec3((m21, m22, m23)), NoeVec3((m04, m14, m24))])
        boneMatrixList.append(boneMtx)
        boneMtx2 = NoeMat43()
        br = boneMtx
        boneMtx2[0] = br[0]
        boneMtx2[1] = br[1]
        boneMtx2[2] = br[2]
        boneMtx2[3] = boneMtx[3]
        boneInvMatrixList.append(boneMtx2)
        Name = St[bs.readInt64()]
        if Name in BoneNames:
            Dups.append(Name)
            Name = Name+"_duplicate_"+str(u)
        BoneNames.append(Name)
        Parent = bs.readInt64()
        UNK1 = bs.readInt64()
        UNK2 = bs.readInt64()
        UNK3 = bs.readInt64()
        UNK4 = bs.readInt64()
        Bone25List.append(NoeBone(u, Name, boneMtx2, None, Parent))
    bs.seek(POS4+Plus)
    for rm in range(0, Count2):
        Bone25Remap.append(bs.readInt())
    #print(Bone25Remap)
    print(Dups)
    return Bone25List, Bone25Remap

def GetUNK29(bs, LOC, Count, St):
    Test2 = []
    bs.seek(LOC)
    for T2 in range(0, Count):
        Mo = Morph()
        Mo.Name = St[bs.readInt64()]
        Mo.Pad = bs.readInt64()
        bs.seek(56, 1)
        Mo.UNK4ID = bs.readInt()
        Mo.Count2 = bs.readInt()
        bs.seek(8, 1)
        Mo.Pad2 = bs.readInt64()
        Test2.append(Mo)
    return Test2

def GetUNK31(bs, LOC, Count, St):
    Test2 = []
    bs.seek(LOC)
    for T2 in range(0, Count):
        Test2.append(St[bs.readInt64()])
    return Test2


def GetSkel(bs, LOC, St):
    boneList = []
    bs.seek(LOC)
    BoneCount = bs.readInt()
    strc = bs.readInt()
    pad = (4 - strc % 4) % 4
    SkelSource = bs.readBytes(strc).decode("ASCII").rstrip("\0")
    bs.seek(pad, 1)
    MatList = []
    BoneNames = []
    ParentList = []
    Sort = []
    Sort2 = []
    SortedBoneList = []
    for B in range(0, BoneCount):
        rot = NoeQuat.fromBytes(bs.readBytes(16)).transpose()
        bs.seek(0, 1)
        pos = NoeVec3.fromBytes(bs.readBytes(12))
        pos[0] = pos[0]
        pos[1] = pos[1]
        pos[2] = pos[2]
        mat = rot.toMat43()
        mat.__setitem__(3,(pos[0],pos[1],pos[2]))
        MatList.append(mat)
        bs.seek(76, 1)
        #MatList.append(bs.readBytes(104))
    for P in range(0, BoneCount):
        Parent = bs.readInt()
        ParentList.append(Parent)
        #print(Parent)
    for PP in range(0, BoneCount):
        ID = bs.readInt()
        Sort.append(ID)
    for Q in range(BoneCount):
        SortedBoneList.append(None)
    for N in range(0, BoneCount):
        BID = bs.readInt()
        BoneC = bs.readInt()
        BoneName = bs.readBytes(BoneC).decode("ASCII").rstrip("\0")
        bs.seek((4 - BoneC % 4) % 4, 1)
        BoneNames.append(BoneName)
        print(BoneName, BID)
        Sort2.append(BID)
    for fuck in range(0, BoneCount):
        Y = Sort2.index(fuck)
        print(fuck, BoneNames[Y])
    for K in range(BoneCount):
        #print(ParentList[K], Sort[K])
        BT = BoneClass()
        BT.ParentID = ParentList[K]
        #BT.Name = BoneNames[Sort[K]-1]
        # BT.Name = St[Sort[K]-1]
        BT.Mat = MatList[K]
        BT.BoneID = Sort[K]-1
        # if K == 0:
        #     SortedBoneList[BoneCount - Sort[K]] = BT
        # else:
        #     SortedBoneList[Sort[K]] = BT
    for Q in range(0, BoneCount):
        # CB = Sort2[Q]
        # Held = St[Sort[Q]]
        #boneList.append(NoeBone(Q, Held, MatList[Q], None, ParentList[Q]))
        boneList.append(NoeBone(Q, "bone_"+str(Q), MatList[Q], None, ParentList[Q]))
    #print("BoneEnd", bs.tell())
    return boneList, Sort
    

def noepyLoadModel(data, mdlList):
    Skin = 1
    bs = NoeBitStream(data)
    ctx = rapi.rpgCreateContext()
    bs.seek(4)
    ObjCount = bs.readInt()
    ObjDataTableLoc = bs.readInt64()
    NameLoc = bs.readInt64()
    Names = GetNames(bs, NameLoc, ObjCount)
    bs.seek(ObjDataTableLoc)
    ObjTables = []
    for Z in range(0, ObjCount):
        ObjTables.append(bs.readInt64())
    #print(ObjTables, Names)
    ObjList = []
    for MM in range(0, len(ObjTables)):
        ObjListBlock = []
        BlockLOC = ObjTables[MM]
        bs.seek(BlockLOC)
        for E in range(0, 44):
            ObjListBlock.append(bs.readUInt64())
        UNK0 = ObjListBlock[0]
        UNK1 = ObjListBlock[1]
        UNK2 = ObjListBlock[2]
        UNK4Count = ObjListBlock[3]
        UNK4 = ObjListBlock[4]+BlockLOC
        UNK5 = ObjListBlock[5]
        AttribLOC = ObjListBlock[6]+BlockLOC
        UNK7 = ObjListBlock[7]
        VertexLOC = ObjListBlock[8]+BlockLOC
        UNK9 = ObjListBlock[9]
        FaceLOC = ObjListBlock[10]+BlockLOC
        BoneMap = ObjListBlock[11]+BlockLOC
        MatC = ObjListBlock[15]
        Mats = ObjListBlock[16]+BlockLOC
        Skel = ObjListBlock[21]+BlockLOC
        B25 = ObjListBlock[25]+BlockLOC
        StringBlockC = ObjListBlock[38]
        StringBlockLOC = ObjListBlock[39]+BlockLOC
        #print(Names[M], UNK4, AttribLOC, VertexLOC, FaceLOC)
        O = ObjData()
        O.AttribLOC = AttribLOC
        O.UNK4LOC = UNK4
        O.UNK4Count = UNK4Count
        O.VLOC = VertexLOC
        O.FLOC = FaceLOC
        O.SubCount = UNK5
        O.MatC = MatC
        O.Mats = Mats
        O.SkelLOC = Skel
        O.BoneMap = BoneMap
        O.Bone25 = B25
        O.StringC = StringBlockC
        O.StringLOC = StringBlockLOC
        O.MorphData = ObjListBlock[29]+BlockLOC
        O.MorphDC = ObjListBlock[28]
        O.MorphC = ObjListBlock[30]
        O.MorphNames = ObjListBlock[31]+BlockLOC
        ObjList.append(O)
        print(O.__dict__)
    V_COL = 128
    V_UV = 8
    V_UV2 = 16
    V_Skin = 512
    V_ID = 1024
    V_COL2 = 256
    for M in range(0, len(ObjList)):
        rapi.rpgReset()
        C = ObjList[M]
        Skip = 0
        print(C.__dict__)
        S = GetStrings(bs, C.StringLOC, C.StringC)
        MM = GetMaterials(bs, C.Mats, C.MatC, S)
        U = GetUNK4(bs, C.UNK4LOC, C.UNK4Count)
        A = GetAttrib(bs, C.AttribLOC, C.SubCount)
        if C.Bone25 == ObjTables[M]:
            B25L, Sort = GetSkel(bs, C.SkelLOC, S)
        else:
            B25L, Sort = GetUNK25(bs, C.Bone25, ObjTables[M], S)
        MD = GetUNK29(bs, C.MorphData, C.MorphDC, S)
        MN = GetUNK31(bs, C.MorphNames, C.MorphC, S)
        print("Attrib", len(A), "UNK4", len(U))
        #print(A, U)
        Add = 0
        MorphTotal = 0
        for X in range(0, len(U)):
            UC = U[X]
            print(UC.__dict__)
            BoneMapL = []
            if UC.MorphCount:
                CMD = MD[MorphTotal]
                MorphTotal += 1
            for SC in range(0, UC.UseCount):
                BoneMapL = []
                CA = A[SC+Add]
                print(CA.__dict__)
                bs.seek(C.BoneMap+(CA.BoneMapPush*2))
                print("BoneMapLOC", (CA.BoneMapPush*2), bs.tell(), CA.BoneMapCount)
                if CA.BoneMapCount:
                    for BML in range(0,CA.BoneMapCount):
                        BoneMapL.append(Sort[bs.readUShort()])
                    rapi.rpgSetBoneMap(BoneMapL)
                    print("Read BoneMap", BoneMapL)
                bs.seek(C.VLOC+CA.VertexPush)
                VertBlock = bs.readBytes(CA.VertexCount*UC.VStride)
                bs.seek(C.FLOC+CA.FacePush)
                FaceBlock = bs.readBytes(CA.FaceCount*2)
                if UC.MorphCount:
                    print(X, len(MN), MorphTotal)
                    MorphStuff(bs, S, UC, SC, CA, FaceBlock, C, MN, CMD)
                print(M, SC, S[UC.UNKID]+"_"+str(SC))
                rapi.rpgSetName(S[UC.UNKID]+"_"+str(SC))
                rapi.rpgSetMaterial(MM[CA.UNKInt[0]].Name)
                normals = bytearray()
                for Q in range(0, CA.VertexCount):
                    normals+= VertBlock[Q*UC.VStride+12:Q*UC.VStride+12+4]
                norm = rapi.decodeNormals32(normals, 4, -10, -10, -10, NOE_LITTLEENDIAN)
                tang = bytearray()
                for T in range(0, CA.VertexCount):
                    tang+= VertBlock[T*UC.VStride+16:T*UC.VStride+16+4]
                tangent = rapi.decodeTangents32(tang, 4, -7, -7, -7, -7, NOE_LITTLEENDIAN)
                rapi.rpgBindPositionBufferOfs(VertBlock, noesis.RPGEODATA_FLOAT, UC.VStride, 0)
                rapi.rpgBindNormalBuffer(norm, noesis.RPGEODATA_FLOAT, 12)
                rapi.rpgBindTangentBuffer(tangent, noesis.RPGEODATA_FLOAT, 12)
                Push = 16
                if UC.DataType & V_UV == V_UV:
                    Push += 4
                    Push2 = Push+2
                    print("UV", Push, Push2)
                    UV = []
                    for n in range(0, CA.VertexCount):
                        UVU = int.from_bytes(VertBlock[n*UC.VStride+Push:n*UC.VStride+Push+2], 'little') * CA.UNKF[0]
                        UVV = int.from_bytes(VertBlock[n*UC.VStride+Push2:n*UC.VStride+Push2+2], 'little') * CA.UNKF[1]
                        UV.append(UVU)
                        UV.append(UVV)
                    UV = struct.pack('f'*len(UV), *UV)
                    rapi.rpgBindUV1Buffer(UV, noesis.RPGEODATA_FLOAT, 8)
                    O = NoeVec3((CA.UNKF[2],CA.UNKF[3],float(1)))
                    rapi.rpgSetUVScaleBias(None, O)
                if UC.DataType & V_UV2 == V_UV2:
                    Push += 4
                    Push2 = Push+2
                    UV = []
                    print("UV2", Push, Push2)
                    for n in range(0, CA.VertexCount):
                        UVU = int.from_bytes(VertBlock[n*UC.VStride+Push:n*UC.VStride+Push+2], 'little') * CA.UNKF[0]
                        UVV = int.from_bytes(VertBlock[n*UC.VStride+Push2:n*UC.VStride+Push2+2], 'little') * CA.UNKF[1]
                        UV.append(UVU)
                        UV.append(UVV)
                    UV = struct.pack('f'*len(UV), *UV)
                    rapi.rpgBindUV2Buffer(UV, noesis.RPGEODATA_FLOAT, 8)
                    O = NoeVec3((CA.UNKF[2],CA.UNKF[3],float(1)))
                    rapi.rpgSetUVScaleBias(None, O)
                if UC.DataType & V_COL == V_COL:
                    Push += 4
                    print("Color", Push)
                    rapi.rpgBindColorBufferOfs(VertBlock, noesis.RPGEODATA_UBYTE, UC.VStride, Push, 4)
                else:
                    VCOL = []
                    for v in range(0, CA.VertexCount):
                        VCOL.append(float(0.0))
                        VCOL.append(float(0.0))
                        VCOL.append(float(0.0))
                        VCOL.append(float(1.0))
                    VCB = struct.pack('f'*len(VCOL), *VCOL)
                    rapi.rpgBindColorBuffer(VCB, noesis.RPGEODATA_FLOAT, 16, 4)
                if UC.DataType & V_COL2 == V_COL2:
                    #Only one Color Buffer can be used
                    Push+= 4
                    #rapi.rpgBindColorBufferOfs(VertBlock, noesis.RPGEODATA_UBYTE, UC.VStride, Push, 4)
                if Skin and UC.DataType & V_ID == V_ID:
                    Push += 4
                    Push2 = Push+4
                    print("Skin", Push, Push2)
                    rapi.rpgBindBoneWeightBufferOfs(VertBlock, noesis.RPGEODATA_UBYTE, UC.VStride, Push, 4)
                    rapi.rpgBindBoneIndexBufferOfs(VertBlock, noesis.RPGEODATA_UBYTE, UC.VStride, Push2, 4)
                if Skin:
                    if CA.BoneMapCount == 1:
                        print("AutoMapWeights")
                        WBlock = []
                        IBlock = []
                        for VV in range(0, CA.VertexCount):
                            IBlock.append(0)
                            IBlock.append(65535)
                        AutoIBlock = struct.pack('H'*len(IBlock), *IBlock)
                        #print(AutoIBlock)
                        rapi.rpgBindBoneWeightBufferOfs(AutoIBlock, noesis.RPGEODATA_USHORT, 4, 2, 1)
                        rapi.rpgBindBoneIndexBufferOfs(AutoIBlock, noesis.RPGEODATA_USHORT, 4, 0, 1)
                rapi.rpgCommitTriangles(FaceBlock, noesis.RPGEODATA_USHORT, CA.FaceCount, noesis.RPGEO_TRIANGLE_STRIP, 1)
                rapi.rpgClearBufferBinds()
            Add += UC.UseCount
            rapi.rpgClearBufferBinds()
        mdl = rapi.rpgConstructModel()
        if B25L:
            B25L = rapi.multiplyBones(B25L)
            mdl.setBones(B25L)
        mdlList.append(mdl)
    return 1

def MorphStuff(bs, S, UC, SC, CA, FaceBlock, C, MN, MT):
    bs.seek((C.VLOC+CA.VertexPush)+(CA.VertexCount*UC.VStride))
    MD = MT
    for Mor in range(0, UC.MorphCount):
        rapi.rpgClearBufferBinds()
        #print(Mor, MN[Mor+MT.Pad], bs.tell())
        rapi.rpgSetName(MN[Mor+MT.Pad])
        MorphNormals = bytearray()
        Morphs = bs.readBytes(CA.VertexCount*UC.VStride)
        for Mo in range(0, CA.VertexCount):
            MorphNormals+= Morphs[Mo*UC.VStride+12:Mo*UC.VStride+12+4]
        norm = rapi.decodeNormals32(MorphNormals, 4, -10, -10, -10, NOE_LITTLEENDIAN)
        rapi.rpgBindPositionBufferOfs(Morphs, noesis.RPGEODATA_FLOAT, UC.VStride, 0)
        rapi.rpgBindNormalBuffer(norm, noesis.RPGEODATA_FLOAT, 12)
                        # rapi.rpgFeedMorphTargetPositionsOfs(Morphs, noesis.RPGEODATA_FLOAT, UC.VStride, 0)
                        #rapi.rpgFeedMorphTargetNormals(MorphNormals, noesis.RPGEODATA_FLOAT, 12)
                        # rapi.rpgCommitMorphFrame(CA.VertexCount)
                    # rapi.rpgCommitMorphFrameSet()
        rapi.rpgBindUV1BufferOfs(Morphs, noesis.RPGEODATA_USHORT, UC.VStride, 20)
        rapi.rpgCommitTriangles(FaceBlock, noesis.RPGEODATA_USHORT, CA.FaceCount, noesis.RPGEO_TRIANGLE_STRIP, 1)
