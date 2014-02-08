Footprint.controller = SC.ObjectController.create();
Footprint.photosController = SC.ArrayController.create({
    allowsMultipleSelection: NO,
    content: [

        SC.Object.create({
            url: "built_form_images/pt_city_mixed_use/photo1.jpg",
            title: "Downtown Oregon"
        }),

        SC.Object.create({
            url: "built_form_images/pt_city_mixed_use/photo2.jpg",
            title: "Redwood City"
        }),

        SC.Object.create({
            url: "built_form_images/pt_city_mixed_use/photo3.jpg",
            title: "Another city"
        })
    ]
});
