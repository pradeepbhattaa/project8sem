
function updateProvinces(country) {
    const provinces = {
        "country1": ["Koshi Pradesh", "Madesh Pradesh", "Bagmati Province", "Gandaki Province", "Lumbini Province", "Karnali Province", "Sudurpaschim Province"]
    };
    updateDropdown('province', provinces[country]);
}

function updateDistricts(province) {
    const districts = {
        "Koshi Pradesh": ["Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", "Okhaldhunga", "Panchthar", "Sankhuwasabha", "Solukhumbu", "Sunsari", "Taplejung", "Terhathum", "Udayapur"],
        "Madesh Pradesh": ["Saptari", "Siraha", "Dhanusha", "Mahottari", "Sarlahi", "Bara", "Parsa", "Rautahat"],
        "Bagmati Province": ["Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu", "Kavrepalanchok", "Lalitpur", "Makwanpur", "Nuwakot", "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok"],
        "Gandaki Province": ["Baglung", "Gorkha", "Kaski", "Lamjung", "Manang", "Mustang", "Myagdi", "Nawalpur", "Parbat", "Syangja", "Tanahun"],
        "Lumbini Province": ["Arghakhanchi", "Banke", "Bardiya", "Dang", "Eastern Rukum", "Gulmi", "Kapilvastu", "Parasi", "Palpa", "Pyuthan", "Rolpa", "Rupandehi"],
        "Karnali Province": ["Dailekh", "Dolpa", "Humla", "Jajarkot", "Jumla", "Kalikot", "Mugu", "Salyan", "Surkhet", "Western Rukum"],
        "Sudurpaschim Province": ["Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura", "Darchula", "Doti", "Kailali", "Kanchanpur"]
    };
    updateDropdown('district', districts[province]);
}

function updateDropdown(id, options) {
    let select = document.getElementById(id);
    select.innerHTML = ''; // Clear previous options
    options.forEach(option => {
        let optionElement = new Option(option, option);
        select.appendChild(optionElement);
    });
    if (options.length > 0) {
        select.dispatchEvent(new Event('change'));
    }
}


