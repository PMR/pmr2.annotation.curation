function appendCurationFlagDictWidget(widgetId)
{
  var widgetName = 'curationflagdict';
  var tag = 'table';
  var divId = '#' + widgetName + '-' + widgetId;

  var curationDiv = jq(divId);
  curationDiv.after('<' + tag + '></' + tag + '>');
  curationDiv.css('display', 'none');

  var textareaId = '#' + widgetId;
  var values = jq(textareaId)[0].innerText.split('\n');
  values.reverse();

  var editor = jq(divId + ' + ' + tag);
  editor.append('<tr><th>Flag Values</th><th>Description</th></tr>');

  while (values.length)
  {
    key = values.pop();
    value = values.pop();
    i = values.length;
    editor.append(
      '<tr id="' + widgetName + '-row' + i + '">' +
      '<td>' +
      '<input type="text" name="' + widgetName + '-key' + i + 
      '" value="' + key + '"/>' +
      '</td>' +
      '<td>' +
      '<input type="text" name="' + widgetName + '-value' + i + 
      '" value="' + value + '"/>' +
      '</td>' +
      '</tr>' +
      '');
  }
}
