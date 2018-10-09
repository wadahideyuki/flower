function thumbnailsHandler(json) {
  var t  = json['thumbnails'];
  var id = json['id'];
  var u  = json['user'];
  var ul = document.createElement('ul');
  for (var i in t) {
    if(!t[i]['thumbnail']) continue;
    var li = document.createElement('li');
    li.setAttribute('class', 'thumbnail_'+i);
    var a = document.createElement('a');
    a.setAttribute('href', t[i]['permalink']);
    a.setAttribute('target', '_blank');
    var img = document.createElement('img');
    img.setAttribute('src', t[i]['thumbnail']);
    a.appendChild(img);
    li.appendChild(a);
    ul.appendChild(li);
  }
  document.write('<div id="'+id+'"></div>');
  var e = document.getElementById(id);
  e.className='thumbnails '+u;
  e.appendChild(ul);
  var clear = document.createElement('hr');
  clear.style.clear = 'both';
  clear.style.visibility = 'hidden';
  e.appendChild(clear);
}