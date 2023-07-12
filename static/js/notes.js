const getPreview = (url) => {
fetch(`https://opengraph.io/api/1.1/site/${encodeURIComponent(url)}`)
  .then(response => response.json())
  .then(data => {
    const imageUrl = data.openGraph.image.url;
    // использовать imageUrl для отображения превью на странице
    return imageUrl;
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
