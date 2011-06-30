%rename(toFloat) Fixed::operator float();

%extend Fixed {
public:
    %pythoncode %{
    def __repr__(self):
        return "%f" % (self.toFloat())
    %}
}
