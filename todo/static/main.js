strikeBtn.on('click', function() {
  $(this).closest('tr').find('.note-td')
  [ this.checked ? 'addClass' : 'removeClass' ]
  ('done')
} )