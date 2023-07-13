const getPreview = (url) => {
fetch(`https://opengraph.io/api/1.1/site/${encodeURIComponent(url)}`)
  .then(response => response.json())
  .then(data => {
    const imageUrl = data.openGraph.image.url;
    // использовать imageUrl для отображения превью на странице
    return imageUrl;
  });
}

function getOpenGraph(url) {
  return fetch(url)
    .then(response => {
      return response.text();
    })
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const og = {
        title: doc.querySelector('meta[property="og:title"]').getAttribute('content'),
        description: doc.querySelector('meta[property="og:description"]').getAttribute('content'),
        image: doc.querySelector('meta[property="og:image"]').getAttribute('content')
      };
      return og;
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function getUrlsFromText(text) {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const urls = text.match(urlRegex);
  return urls;
}

const addOpenGraph = (div, url) => {
// TODO:  Добивать это всё в DIV программно!!!
  const ogData = document.createElement('div');
  ogData.classList.add('og-data');
  const ogTitle = document.createElement('div');
  ogTitle.classList.add('og-title');
  const ogDescription = document.createElement('div');
  ogDescription.classList.add('og-description');
  const ogImage = document.createElement('div');
  ogImage.classList.add('og-image');
  ogData.appendChild(ogTitle);
  ogData.appendChild(ogDescription);
  ogData.appendChild(ogImage);
  div.appendChild(ogData);
  getOpenGraph(url)
    .then(og => {
      ogTitle.innerText = og.title;
      ogDescription.innerText = og.description;
      ogImage.src = og.image;
      ogData.style.display = 'block';
    });
  }


const ajax = (args = {}) => {
  let method = "POST";
  if (args.method) {
    method = args.method;
  }
  const responseType = args.responseType || "text";
  const defaultError = (event) => {
    alert(`Error: ${event}`);
  };
  const xhr = new XMLHttpRequest();
  let params = "";
  if (args.data) {
    params = new URLSearchParams(args.data).toString();
  }
  xhr.open(method, args.url, true);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  if (args.headers) {
    Object.entries(args.headers).forEach((entry) => {
      [key, value] = entry;
      xhr.setRequestHeader(key, value);
    });
  }
  xhr.responseType = responseType;
  console.log(`Ajax (${method}) ${args.url} p: ${params}`);
  xhr.send(params);
  xhr.onload = function () {
    args.success(xhr.response);
  };
  if (args.error) {
    xhr.onerror = function () {
      args.error(xhr.response);
    };
  } else {
    xhr.onerror = defaultError;
  }
};
