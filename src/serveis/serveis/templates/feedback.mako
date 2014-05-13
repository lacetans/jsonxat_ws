<h1>App Feedback</h1>

% if message:
<div class="message">
    ${message}
</div>
% endif

% if renderer:
    ${renderer.begin(request.resource_url(request.root, 'feedback'))}
    ${renderer.csrf_token()}

    <%
    from formencode import Schema, validators
    fields = renderer.form.schema.fields
    %>
    % for field in fields.keys():
    <div class="field">
        ${renderer.label( field )} :
        ${renderer.errorlist( field )}
        % if type(fields[field])==validators.UnicodeString:
            ${renderer.text( field, size=30)}
        % elif type(fields[field])==validators.OneOf:
            ${renderer.select( field, fields[field].list )}
        % else:
            ${renderer.text( field, size=30)}
        % endif
        <!-- TODO: textareas?, file, etc. -->
    </div>
    % endfor
    
    <div class="buttons">
        ${renderer.submit("submit", "Submit")}
    </div>
    ${renderer.end()}

% endif
