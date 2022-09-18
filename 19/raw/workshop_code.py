import random, math

def creturn(m, f, s):
    eta = 0.5
    retu = eta*m*f*s
    return retu

def fout(v, q):
    alfa = 0.7
    beta = 0.2
    e = 0.2
    o = alfa*v + beta*q + (1 - alfa - beta)*e 
    return o

def aspir(ga, ah, ass):
    ah = ga*ah + (1- ga)*ass
    return ah

def fprob(oo, aa):
    a = 0.6
    b = 0.4
    gg = a + b*( oo - aa )
    pp = 1/(1 + math.exp(gg))
    return pp

def cprob(avgk, sums):
    if (sums == 0):
        pp = 0
    else:
        pp = avgk / sums
    return pp

## fundamental conditions
aah = 0
out = [] # performance outcome of flim
ret = [] # consultant’s return
probc = [] # the probability that a firm will select consultant
probf = [] # the probability of abandonment
oit = []
pool = [] # innovation pool
con = [] # innovation of consultant
firm = [] # innovation of firm
on = [] # selected inno.
selected = [] # supply inno.
match = [] # choice of firm
trans = [] # transaction between consultant and firm
vvd = []
qqd = []
mmvd = []
zeta = 0.8
cconn = []

#make inno. pool
for m in range(0,10):     #####
    pool.append(m)
    on.append(0)
print("pool:"+str(pool))

for t in range(0,10):     #####
    cret = []
    fac = []
    fprobabi = []
    cac = []
    cprobabi = []

    # step1 consultants have acurrent innovation they supply
    for c in range(0, 10):     #####
        if len(pool) >= 2:
            chosen = random.randrange(len(pool)-1)
            con.append(pool[chosen])
            on[chosen] = 1
        else:
            con.append(0)
            on[0] = 1                    
    print("con:"+str(con))

    # mark chosen inno.
    var = 0
    for x in on:
        if x == 1:
            selected.append(pool[var])
        var +=1

    # step2 firms have a current innovation they demand
    for f in range(0, 1):     #####
        if len(selected) >= 2:
            chosen = random.randrange(len(selected)-1)
            firm.append(selected[chosen])
        else:
            firm.append(selected[0])
    print("firm:"+str(firm))

    # step3 firms and consultants are matched
    choice = []
    for r in firm:
        var = 0
        
        for c in con:
            if r == c:
                choice.append(var)
            var +=1
        match.append(choice)
        choice=[]
    print("match:"+str(match))

    choice=[]
    var = 0
    m = 0
    for r in match:
        choice.append(var)
        m = random.randrange(len(match[var]))
        choice.append(match[var][m])
        trans.append(choice)
        choice=[]
        var+=1
    print("trans:"+str(trans))

    for t in range(0,300):

        cret = []
        fac = []
        fprobabi = []
        cac = []
        cprobabi = []
        oit = []
    

    # step4 each consultant receives a return based on demand for its services
    for kk in range(0, len(con)):
        innov = con[kk]
        team = kk

        # the number of firms pursuing innovation j
        for i in range(0, len(firm)):
            if (firm[i] == innov):
                k = 1
            else:
                k = 0
            t = t + k
        s = t
        t = 0

        # the number of consultants offering innovation j
        for i in range(0, len(con)):
            if (con[i] == innov):
                k = 1
            else:
                k = 0
            t = t + k
        f = t
        t = 0

        # the number of clients served by consultant c
        t = 0
        for i in range(0, len(firm)):
            if (trans[i][0] == team):
                k = 1
            else:
                k = 0
            t = t + k
        m = t
        t = 0

        cret.append( creturn(m, f, s) )

    # step 5 each firm receives a outcome based on its performance
    vdv = 0
    qdq = 0
    for k in range(0, len(firm)):
        v = firm[k]*0.5 + 0.5
        q = trans[k][1]*0.5 + 0.5
        oit.append(fout(v, q))

        vdv = vdv + v
        qdq = qdq + q
    vvd.append(vdv/len(firm))
    qqd.append(qdq/len(firm)/40)

    # step 6 con decide (in light of their out comes) whether to continue to utilize their current innovation versus abandon it for an alternative 
    for k in range(0, len(con)):
        team = k
        sws = []
        for i in range(0, len(firm)):
            if ( trans[i][1] == team):
                ddp = trans[i][1]
                sws.append(ddp)
        dds = 0
        for i in range(0, len(sws)):
            ssf = cret[ sws[i] ]
            dds = dds + ssf
        if ( len(sws) == 0 ):
            avgk = 0
        else:
            avgk = dds / len(sws)
        sdg = 0
        pdg = 0
        for i in range(0, len(con)):
            if (con[i] == innov):
                ffg = cret[i]
                sdg = sdg + ffg
                pdg += 1
        if (pdg == 0):
            sums = 0
        else:
            sums = sdg / pdg
        ccpr = cprob(avgk, sums)
        cprobabi.append( ccpr )

        ffn = 0
        for i in range(0, len(con)):
            sns = cret[i] 
            ffn = ffn + sns
        if (ffn == 0):
            ass = 0
        else:
            aas = 1 / ( (len(con)-1)*ffn )
        aah = (1- zeta)*aah + zeta*cret[team]
        ccac = aspir(0.3, aah, aas)
        cac.append( ccac )

        if (ccpr >= ccac):
            pass
        else:
            sds = random.randrange(10)
            if (sds < 5):
                con[k] = random.randrange(len(pool)-1)
            else:
                lll = cret.index( max(cret) )
                con[k] = con[lll]

    # step 7 firm decide (in light of their returns) whether to continue to offer their current innovation versus abandon it foranal ternative
    for k in range(0, len(firm)):
        innov = firm[k]
        team = k

        ffn = 0
        for i in range(0, len(firm)):
            sns = oit[i] 
            ffn = ffn + sns
        aas = 1 / ( (len(firm)-1)*ffn )
        aah = (1- zeta)*aah + zeta*oit[team]
        ffac = aspir(0.3, aah, aas)
        fac.append( ffac )

        ffpr = fprob(oit[k], aah)
        fprobabi.append( ffpr )

        if (ffpr >= ffac):
            mmm = random.random() 
            if (mmm < ffpr):
                sds = random.randrange(10)
                if (sds < 5):
                    hh = random.randrange(len(con)-1)
                    firm[k] = con[hh]
                    vvv = []
                    for m in range(0, len(con) ):
                        if (con[m] == firm[k]):
                            vvv.append(m)
                        match[k] = vvv
                    io = random.randrange(len(vvv))
                    trans[k][1] = vvv[io]
                else:
                    lll = oit.index( max(oit) )
                    firm[k] = firm[lll]
            else:
                pass
            
        else:
            sds = random.randrange(10)
            if (sds < 5):
                hh = random.randrange(len(con)-1)
                firm[k] = con[hh]
                vvv = []
                for m in range(0, len(con) ):
                    if (con[m] == firm[k]):
                        vvv.append(m)
                    match[k] = vvv
                io = random.randrange(len(vvv))
                trans[k][1] = vvv[io]

            else:
                lll = oit.index( max(oit) )
                firm[k] = firm[lll]
    
    for ii in range(0, len(firm)):
        mmvd.append(firm[ii])
