CurationFlagDictCounter = new function f()
{
  this.counter = 0;
  this.next = function()
  {
    result = this.counter;
    this.counter = this.counter + 1;
    return result;
  };
}

function appendWidgetRow(selector, widgetName, key, value)
{
  var i = CurationFlagDictCounter.next()
  var editor = jq(selector);
  var rowid = widgetName + '-row' + i
  editor.append(
    '<tr id="' + rowid + '">' +
    '<td>' +
    '<input type="text" name="' + widgetName + '-key' + i + 
    '" value="' + key + '"/>' +
    '</td>' +
    '<td>' +
    '<input type="text" name="' + widgetName + '-value' + i + 
    '" value="' + value + '"/>' +
    '</td>' +
    '<td>' +
    '<button type="button" value="delete" ' +
    'onclick="javascript:deleteWidgetRow(\'' + selector + ' > #' + rowid + 
    '\')">delete</button>' +
    '</td>' +
    '</tr>' +
    '');
  return i;
}

function deleteWidgetRow(rowid)
{
  jq(rowid).remove();
}

function appendNewWidgetRow(selector, widgetName)
{
  row = appendWidgetRow(selector, widgetName, '', '');
  jq(selector + ' [name=' + widgetName + '-key' + row + ']').select();
}

function calcCurationFlagDictWidget(widgetId)
{
  // FIXME define this inside some sort of object to avoid repetition
  var widgetName = 'curationflagdict';
  var tag = 'table';
  var divId = '#' + widgetName + '-' + widgetId;
  var selector = divId + ' + ' + tag + ' > tbody input';

  var inputs = jq(selector);
  results = '';
  for (var i = 0; i < inputs.length; i++) {
    results = results + inputs[i].value + '\n';
  }
  jq('#' + widgetId).val(results);
}

function appendCurationFlagDictWidget(widgetId)
{
  // FIXME define this inside some sort of object to avoid repetition
  var widgetName = 'curationflagdict';
  var tag = 'table';
  var divId = '#' + widgetName + '-' + widgetId;

  var curationDiv = jq(divId);
  curationDiv.after('<' + tag + '></' + tag + '>');
  curationDiv.css('display', 'none');

  var textareaId = '#' + widgetId;
  var values = jq(textareaId).val().split('\n');
  values.reverse();

  var structure = jq(divId + ' + ' + tag);
  structure.append('<thead><tr><th>Flag Values</th>' +
                   '<th>Description</th></tr></thead>');
  structure.append('<tbody></tbody>');

  var selector = divId + ' + ' + tag + ' > tbody';

  while (values.length) {
    key = values.pop();
    value = values.pop() || '';
    if (key) {
      // as key cannot be null.
      appendWidgetRow(selector, widgetName, key, value);
    }
  }
  structure.append(
    '<tfoot><tr><th colspan="2"><button type="button" value="New Flag" ' +
    'onclick="javascript:appendNewWidgetRow(\'' + selector + '\', \'' + 
    widgetName + '\')">New Flag</button></th></tr>');
  jq(textareaId).parents('form').bind(
    'submit', function f() {calcCurationFlagDictWidget(widgetId)});
}

