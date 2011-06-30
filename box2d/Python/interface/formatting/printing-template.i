    %%extend %s {
    public:
        %%pythoncode %%{
        def __repr__(self):
            return %s
        %%}
    }
