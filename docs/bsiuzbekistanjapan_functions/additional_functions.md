# Additional functions

0. Have the users enter the contents of the posts

1. Implement tracking statuses for the posts
    1. Arrived in BSI office
    2. The post is on the way
    3. Arrived in Tashkent
    4. Delivered
   
2. Add two extra fields when entering a new weight
    1. On whose behalf the post is sent
    2. The recipient of the post
 
3. Define human readable unique ID to identify posts
```python
    <FROM><TO><USERNAME><USER ID><DATE><INCREMENTAL NUMBER>
```
   
4. Allow admins to give discounts to the preferred clients

5. Mark the flight capacity for allowing posts
    1. Double circle means lots of space, 100% free
    2. Circle means 70% free space
    3. Triangle means 50% free space
    4. Cross means no space to accept posts, posts will be delayed to the next flight