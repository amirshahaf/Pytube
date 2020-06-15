document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#download-form').onsubmit = () => {
        const btn = document.querySelector('#download-btn')
        var spinner = document.createElement('span');
        spinner.className = 'spinner-grow spinner-grow-sm';
        btn.innerHTML = 'loading...';
        btn.disabled = true;
        btn.appendChild(spinner);

        const request = new XMLHttpRequest();
        const link = (document.querySelector('#link').value).replace('https://www.youtube.com/watch?v=', '');
        const resolution = document.querySelector('#resolution').value;
        const request_link = '/api/'+ link + '/' + resolution
        console.log(request_link)
        request.open('GET', request_link);

        request.onload = () => {
            const response = JSON.parse(request.responseText);
            window.location.href = response.link;
        }

        const data = new FormData();
        data.append('link', link)
        data.append('resolution', resolution)

        request.send(data)
        
        return false
    }
})
