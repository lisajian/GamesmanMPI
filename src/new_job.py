class Job:
    """
    A job has a game state, parent, type, and also has a priority for placing
    jobs in a queue for the processes to work on.
    """

    __slots__ = ['job_type', 'parent', 'job_id', 'gs_pos', 'gs_prim', 'gs_remoteness']

    # A list of possible job types.
    FINISHED          = 0
    LOOK_UP           = 1
    RESOLVE           = 2
    SEND_BACK         = 3
    DISTRIBUTE        = 4
    CHECK_FOR_UPDATES = 5

    # Special number associated with the initial job id.
    INITIAL_JOB_ID = 0

    def __init__(self, job_type, parent=None, job_id=None, pos_prim_rem_tup=(None, None, None)):
        """
        Params
        ------

        pos_prim_rem_tuple : (position, primitive, remoteness)
        """
        self.job_type   = job_type
        self.parent     = parent
        self.job_id     = job_id
        self.gs_pos  = pos_prim_rem_tup[0]
        self.gs_prim = pos_prim_rem_tup[1]
        self.gs_remoteness = pos_prim_rem_tup[2]

    def __lt__(self, other):
        """
        Compares two Job objects based off the priority
        they have.
        """
        return self.job_type < other.job_type

    def __str__(self):
        return str((self.gs_pos, self.gs_prim, self.gs_remoteness))
