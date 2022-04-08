for post in `ls ./split*`; do
    echo $post

    curl -XPOST -u 'wb_user:Qaz12345!' 'https://search-wb-elk2-2tlkdepxjo4raohpx44dhowvjm.us-west-2.es.amazonaws.com/_bulk' --data-binary @${post} -H 'Content-Type: application/json'

    echo loaded $post

    sleep 5
done
