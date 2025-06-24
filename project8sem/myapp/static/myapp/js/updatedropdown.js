
    // JavaScript for updating dropdowns
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

    function updateDropdown(dropdownId, optionsArray) {
        let dropdown = document.getElementById(dropdownId);
        dropdown.innerHTML = '';
        optionsArray.forEach(function(option) {
            let optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            dropdown.appendChild(optionElement);
        });
    }

    // Function to navigate between form pages
    function nextPage() {
        // Validate dropdown selections
        const country = document.getElementById('country').value;
        const province = document.getElementById('province').value;
        const district = document.getElementById('district').value;

        if (!country || !province || !district) {
            alert('Please select Country, Province, and District.');
            return;
        }

        document.getElementById('page1').style.display = 'none';
        document.getElementById('page2').style.display = 'block';
    }

    function previousPage() {
        document.getElementById('page1').style.display = 'block';
        document.getElementById('page2').style.display = 'none';
    }

